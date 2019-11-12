import struct
import Config
import Encoder
from Util import *
"""-----------------------------------------------------------------------------/ /-------
|  2 byte   | 1B  |  2 bytes |  2 bytes  |      4 bytes     |  1/0 byte  |               |
--------------------------------------------------------------------------------/ /-------
|  checksum | Flg |  SEQ NUM |  ACK NUM  |      length      |   padding  |    payload    |
--------------------------------------------------------------------------------/ /----"""

"""
length = total_len -11 - 0/1
"""

"""
Flag
| ACK | SYN | SEG |... 5 bits left
"""

class Packet(object):
    def __init__(self, data):
        itr = PacketIterator(data, '>')
        self.checksum = itr.next('H', 2)
        flag = itr.next('B', 1)
        self.ACK = (flag & 0x80) >> 7
        self.SYN = (flag & 0x40) >> 6
        self.SEG = (flag & 0x20) >> 5
        self.seq_num = itr.next('H', 2)
        self.ack_num = itr.next('H', 2)
        self.length  = itr.next('I', 4)
        if self.length & 1 != 1:
            self.padding = itr.next('B', 1)
        
        self.payload = itr.next(str(self.length)+'s', self.length)
        
        self.data = data

    def toBytes(self):
        return self.data

    def __str__(self):
        return "checksum={}\nACK={}\nSYN={}\nSEG={}\nseq_num={}\nack_num={}\nlength={}\npayload={}\n".format(
            self.checksum, self.ACK, self.SYN, self.SEG, self.seq_num, self.ack_num, self.length, self.payload
        )

if __name__ == "__main__":
    testdata = "中文"
    data = Encoder.MAKE_PACKET(ACK=1, SYN=0, SEQ_NUM=2000, ACK_NUM=1, payload=testdata)
    packet = Packet(data)
    print(packet)