import Config
import struct

class PacketIterator(object):
    def __init__(self, data, endian):
        self._endian = endian
        self._offset = 0
        self._data = data
        self._len = len(data)
        
    def next(self, struct_format, data_length):
        if(self._offset + data_length > self._len):
            return None
        tmp_struct = struct.Struct(self._endian + str(self._offset) + "s" + struct_format)
        self._offset += data_length
        return tmp_struct.unpack_from(self._data)

