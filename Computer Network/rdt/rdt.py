from udp import UDPsocket
from timer import timeoutMonitor
import Encoder
import Decoder
import time
import threading
import queue
import Debug
from Util import *
"""

---------------------| |-------------------  -------------------------
 | X | X | X | X | X | | A | A | A | A | A  <<  S | S | S | S | S | S 
---------------------| |-------------------  -------------------------
                       ↑
                   base_seq_num

#############
#  Timeout  #
#############

                          1.Timeout
                            |                                        
recv_thread                 |                          send_thread
  | ↓↓↓ |                   ↓                            |     |
  |     |                  ----------                    | ↑↑↑ |
  | ↓↓↓ |                  |        |                    |     |
  |     |   recv_packet()  | Socket |    send_packet()   | ↑↑↑ |
  |  →  -----------------> |        |  ----------------> |     |
  |-----|                  ----------                    | ↑↑↑ |
                            |                               ↑ 4.1 send all pkt to unsent_queue
                            | 2. _retransmit()              ↑ 
                            ↓                               ↑          ||=
                        --------------------------------    ↑        -------
                        |3.get all pkt in unacked_queue| →→→↑-----→ |   |   | 4.2 also restart the timer
                        --------------------------------            |   ·   |
                                                                    |  /    |
                                                                     -------


############
#  Window  #
################################################################################################

    pkt.ack_num > self.base_seq_num
            -------------------      ------------------------
    ------  A | A | A | A | A   ←---  S | S | S | S | S | S 
    |       -------------------  ↑   ------------------------
    ↓                            |
  _move_window() ----------------O->>Blocked until retransmission is done<<

#################################################################################################

   send_packet_fromQueue <O> Only when the unacked queue is empty
            -------------------      ------------------------
            |               ←--- ←---  S | S | S | S | S | S 
            -------------------      ------------------------

#################################################################################################

            -------------------      ------------------------      send_packet()
            A | A | A | A | A          S | S | S | S | S | S    ←----------------- | S |
            -------------------      ------------------------

#################################################################################################

                   -------------------      ------------------------      
udt_send() ←-----←- A | A | A | A | A ←-     S | S | S | S | S | S    
                |  ------------------- |    ------------------------
                ----→--→--→--→--→--→--→|
                      _retransmit() <O> Highest priority

#################################################################################################

            -------------------        ------------------------    
             A | A | A | A | A          S | S | S | S | S | S    
            -------------------        ------------------------

#################################################################################################
                                                                                                                                                                """

lock = threading.Lock()

class socket():
# init
    def __init__(self):
        # udt
        self.udpsocket = UDPsocket()

        # FSM variables
        self.window_size = Config.RFT_WINDOW_SIZE
        self.unacked_queue = queue.Queue(self.window_size)
        self.unsent_queue = queue.Queue()
        self.base_seq_num = 0
        self.ack_num = 0 # the expecting seq_num

        # timer
        self.timer = timeoutMonitor(self, Config.RDT_TIMEOUT, Config.RDT_TIMROUT_CHECKING_TIME)
        self.timer.start()

        # destination
        self.addr = None

        # receive thread
        self.receive_queue = queue.Queue()

        # flag
        self.SYN_blocked_queue = queue.Queue()

        # coding
        self.encoding = Config.DEFAULT_CODING

        # threads
        self.recv_thread = recv_thread(self)
        self.send_thread = send_thread(self)
        self.retransmit_on = False

# callable method

    def set_encoding(self, encoding):
        self.encoding = encoding

    def bind(self, ip_and_port):
        self.addr = ip_and_port
        self.udpsocket.bind(ip_and_port)
        self.recv_thread.start()

    def _get_base_seq_num(self):
        rtn = self.base_seq_num
        return rtn       

    def accpet(self):
        Debug.verbose_print("accept : Waiting for new connection on {}".format(self.addr))

        # Wait for a connecting request
        packet, addr = self.recv_packet()
        self.addr = addr
        self.send_thread.start()
        Debug.verbose_print("accept : Accept connection from {}".format(addr))
        
        #Send SYN_ACK_PACKET
        self.send_packet(Encoder.SYN_ACK_PACKET(), addr) # SEQ_NUM=self._get_base_seq_num(), ACK_NUM=self.ack_num
        
        self.SYN_blocked_queue.get()
        Debug.verbose_print("accept : Successfully finish handshaking")
        self.ack_num = 1

    def close(self):
        self.recv_thread.terminate()
        self.send_thread.terminate()

    def connect(self, addr):
        self.addr = addr
        Debug.verbose_print("connect : Try to connect {}".format(addr))
        # Send SYN
        self.send_packet(Encoder.SYN_PACKET(), addr) #SEQ_NUM=self._get_base_seq_num(), ACK_NUM=self.ack_num
        self.send_thread.start()

        # Receive SYN ACK
        data, addr = self.recv_packet()
        Debug.verbose_print("connect : Successfully finish handshaking")
        self.ack_num = 1
        
    def recv(self):
        packet, addr = self.recv_packet()
        if packet.SEG == 0:
            return packet.payload.decode(self.encoding)
        else: # packet.SEG == 1
            rtn_payload = packet.payload
            while packet.SEG != 0:
                packet, addr = self.recv_packet()
                rtn_payload += packet.payload # 

            return rtn_payload.decode(self.encoding)

    def send(self, data:str):
        segment_size = Config.SEGMENT_SIZE
        total_len = len(data)

        if total_len < segment_size: 
            self.send_packet(self._make_packet(data), self.addr)
        else:
            ptr = 0
            next_ptr = segment_size
            # data_list = list(data)
            seq_num = self._get_base_seq_num()
            while ptr < total_len:
                seg = 1
                if next_ptr >= total_len: # This is the last packet
                    next_ptr = total_len
                    seg = 0 

                self.send_packet(self._make_packet(data[ptr:next_ptr], seq_num=seq_num, seg=seg), self.addr)

                seq_num += 1
                ptr = next_ptr
                next_ptr += segment_size

    def recv_packet(self):
        receive_bytes = self.receive_queue.get()
        return receive_bytes

    def recv_packet_toQueue(self):  
        while True: # Keep receiving until the packet is in order and not corrupted
            recv = self.udpsocket.recvfrom(Config.BUFSIZE)
            
            # 1. Packet loss -> receive again
            if recv == None: 
                Debug.debug_print("recv_packet : Loss. receive again.")
                continue
            data, addr = recv
            
            # 2. Corrputed -> discard -> receive again
            if Encoder._isCorrupted(data):
                Debug.debug_print("recv_packet : corrupted, discard.")
                continue
            
            # 3. Out of order -> discard -> receive again
            packet = Decoder.Packet(data)     
            Debug.debug_print("recv_packet : (s:{}, a:{}) payload:{}, SYN={}, ACK={}".format(packet.seq_num, packet.ack_num, packet.payload, packet.SYN, packet.ACK))
            if packet.seq_num != 0xFFFF and packet.seq_num > self.ack_num: 
                Debug.debug_print("recv_packet : s:{}. expecting {}, discard".format(packet.seq_num, self.ack_num))
            
            # 4. already receive before -> send pure ack -> receive again
            elif packet.seq_num < self.ack_num: #
                Debug.debug_print("recv_packet : s:{} is already received. expecting {}, discard".format(packet.seq_num, self.ack_num))
                if (packet.SYN == 0 and packet.ACK == 0) or (packet.SYN == 1 and packet.ACK == 1):
                    self.send_pure_ack()
            
            # successfully receive the right packet
            else:
                break
        
        Debug.debug_print("recv_packet : successfully receive reilable packet. seq_num:{}".format(packet.seq_num))

        # ack an unacked packet if (ack_num - 1 equals to smallest base_seq_num)
        if packet.ack_num > self.base_seq_num: 
            # if retransmission is going on, wait until it finishes.
            while True:
                time.sleep(0.01)
                if self.retransmit_on:
                    continue
                else:
                    break
            while self.base_seq_num != packet.ack_num:
                Debug.debug_print("recv_packet : base_seq_num:{}. received ack_num:{}, move window.".format(self.base_seq_num, packet.ack_num))
                self.timer.start_timer()
                self._move_window()
        
        # pure ack
        if packet.ACK == 1 and packet.SYN == 0:
            if packet.ack_num ==1 and packet.seq_num == 0xFFFF: # Only for handshaking sessions
                self.SYN_blocked_queue.put(0)
            Debug.debug_print("recv_packet : pure ack")
            return None # Do not forward ack
            
        # If the packet is not an ACK and not a SYN packet. Send ACK to this packet
        # assert packet.seq_num == self.ack_num
        if (packet.SYN == 0 and packet.ACK == 0) or (packet.SYN == 1 and packet.ACK == 1):
            # expecting the next 
            self.ack_num += 1
            self.send_pure_ack()

        Debug.debug_print("recv_packet : forward to upper layer.")
        return packet, addr # deliver to the upper layer

    def _move_window(self):
        self.base_seq_num += 1
        
        if not self.unacked_queue.empty():
            pkt = Decoder.Packet(self.unacked_queue.get())
            Debug.debug_print("ack and dequeue seq_num:{}".format(pkt.seq_num))
        if not self.unsent_queue.empty():
            sending_pkt_byte = self.unsent_queue.get()
            self.unacked_queue.put(sending_pkt_byte)
            self.udpsocket.sendto(sending_pkt_byte, self.addr)
            #
            packet = Decoder.Packet(sending_pkt_byte)
            Debug.debug_print("send_packet : (s:{}, a:{}) payload:{}".format(packet.seq_num, packet.ack_num, packet.payload))

    def send_packet(self, packet_byte:bytes, addr):
        Debug.debug_print("Append s:{} to unsent_queue".format(Decoder.Packet(packet_byte).seq_num))
        self.unsent_queue.put(packet_byte)

    def send_packet_fromQueue(self):
        if self.unacked_queue.empty() and ( not self.retransmit_on):
            while (not self.unacked_queue.full()) and (not self.unsent_queue.empty()):
                sending_pkt_byte = self.unsent_queue.get()
                self.unacked_queue.put(sending_pkt_byte)
                self.udpsocket.sendto(sending_pkt_byte, self.addr)
                #
                packet = Decoder.Packet(sending_pkt_byte)
                Debug.debug_print("send_packet : (s:{}, a:{}) payload:{}".format(packet.seq_num, packet.ack_num, packet.payload))

    def send_pure_ack(self):
        Debug.debug_print("direct send ACK, ack_num : {}".format(self.ack_num))
        self.udpsocket.sendto(Encoder.ACK_PACKET(SEQ_NUM=0xFFFF, ACK_NUM=self.ack_num), self.addr)

    def _retransmit(self):
        self.timer.start_timer()
        if self.unacked_queue.qsize() == 0:
            return None
        Debug.debug_print("_retransmit : timeout. expecting:{}. {} unacked packet still in queue".format(self.base_seq_num, self.unacked_queue.qsize()))
        cnt = self.unacked_queue.qsize()

        self.retransmit_on = True

        for _ in range(cnt):
            packet_bytes = self.unacked_queue.get()
            self.unacked_queue.put(packet_bytes)

            packet = Decoder.Packet(packet_bytes)
            Debug.debug_print("_retransmit : s:{}, a:{}".format(packet.seq_num, packet.ack_num))

            self.udpsocket.sendto(packet_bytes, self.addr)

        self.retransmit_on = False

        
    def _make_packet(self, data:str, seq_num=-1, seg=0):
        if seq_num == -1:
            seq_num = self._get_base_seq_num()
        Debug.debug_print("_make_packet : make new packet s:{}, a:{}".format(seq_num, self.ack_num))
        return Encoder.MAKE_PACKET(ACK=0, SYN=0, SEQ_NUM=seq_num, ACK_NUM=self.ack_num, payload=data, SEG=seg)

class recv_thread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.RUN = True

    def run(self):
        while self.RUN:
            received_bytes = self.socket.recv_packet_toQueue()
            if received_bytes == None:
                continue
            self.socket.receive_queue.put(received_bytes)

    def terminate(self):
        self.RUN = False

class send_thread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.RUN = True
    
    def run(self):
        while self.RUN:
            self.socket.send_packet_fromQueue()

    def terminate(self):
        self.RUN = False

if __name__ == "__main__":
    # q = queue.Queue()
    # i = 0
    # for _ in range(5):
    #     q.put(i)
    #     i += 1
    # for _ in range(5):
    #     print(q.get())
    pass