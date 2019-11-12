import Config
import struct

class PacketIterator(object):
    def __init__(self, data, endian, offset=0):
        self._endian = endian
        self._offset = offset
        self._data = data
        self._len = len(data)
        
    def next_tuple(self, struct_format, data_length):
        """
        data_length : the standard size (byte) of the struct_format. For example, if struct_format is 'H', then data_length should be 2
        The first element in the returned tuple is useless
        """
        # if Config.DEBUG:
        #     print(self._endian + str(self._offset) + "s" + struct_format)

        if(self._offset + data_length > self._len):
            if Config.DEBUG:
                print("_offset + data_length = ", (self._offset + data_length), 'while data_length is', self._len)
            return None
        
        tmp_struct = struct.Struct(self._endian + str(self._offset) + "s" + struct_format)
        self._offset += data_length
        return tmp_struct.unpack_from(self._data)

    def next(self, struct_format, data_length):
        return self.next_tuple(struct_format, data_length)[1]

    def hasNext(self):
        return self._len > self._offset