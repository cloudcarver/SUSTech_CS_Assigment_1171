from Util import *
from numpy import random
import struct

def MAKE_PACKET(ACK, SYN, SEQ_NUM,ACK_NUM, payload, SEG=0):
    flag = _get_flag(ACK, SYN, SEG)
    if payload != None:
        payload = payload.encode()
        length = len(payload)
    else:
        length = 0
    data = struct.pack('>BHHI', flag, SEQ_NUM, ACK_NUM, length)

    if length & 1 == 0: # Add padding
        data = struct.pack('>9sB', data, 0)

    if payload == None:
        pass
    else:
        data = struct.pack('>'+str(len(data))+'s'+str(length)+'s', data, payload)

    checksum = get_checksum(data)
    pkt =  struct.pack('>H'+str(len(data))+'s', checksum, data)

    return pkt
            

def SYN_PACKET(SEQ_NUM=0, ACK_NUM=0):
    return MAKE_PACKET(0, 1, SEQ_NUM, ACK_NUM, None)
        

def SYN_ACK_PACKET(SEQ_NUM=0, ACK_NUM=1):
    return MAKE_PACKET(1, 1, SEQ_NUM, ACK_NUM, None)


def ACK_PACKET(SEQ_NUM=1, ACK_NUM=1):
    return MAKE_PACKET(1, 0, SEQ_NUM, ACK_NUM, None)

def _get_flag(ACK, SYN, SEG) -> bytes:
    return ((ACK << 7) + (SYN << 6)) + (SEG << 5)& 0xFF

def get_checksum(data) -> bytes:
    itr = PacketIterator(data, '>')
    max_val = 2**16
    sum_val = 0
    while itr.hasNext():
        sum_val += itr.next('H', 2)
        while sum_val >= max_val:
            sum_val %= max_val
            sum_val += 1
    return sum_val ^ 0xFFFF

def _isCorrupted(data):
    # Check the length of the data
    itr = PacketIterator(data, '>')
    itr.next('7s', 7)
    length = itr.next('I', 4)
    total_len = len(data)
    if total_len - 11 != length and total_len - 12 != length:
        return True

    itr = PacketIterator(data, '>')
    max_val = 2**16
    sum_val = 0
    while itr.hasNext():
        sum_val += itr.next('H', 2)
        while sum_val >= max_val:
            sum_val %= max_val
            sum_val += 1
    return sum_val != max_val-1

def _corrupt(data: bytes) -> bytes:
    raw = list(data)
    for i in range(0, random.randint(1, 3)):
        pos = random.randint(0, len(raw) - 1)
        raw[pos] = random.randint(0, 255)
    return bytes(raw)

import Decoder
if __name__ == "__main__":
    pkt_bytes = MAKE_PACKET(1, 1, 0, 0, None)
    print(_isCorrupted(pkt_bytes))

    total = 10_000
    cnt = 0
    for _ in range(total):
        cd = _corrupt(pkt_bytes)
        if not _isCorrupted(cd):
            print("before:",pkt_bytes)
            print("after :",cd)
            pkt = Decoder.Packet(pkt_bytes)
            print(pkt)
            cnt += 1

    print(str((100*cnt/total)) + "%")
    
