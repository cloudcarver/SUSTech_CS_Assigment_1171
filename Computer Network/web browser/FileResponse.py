import mimetypes
import os
import config

class FileResponse(object):
    def __init__(self, abspath, chunked=False, begin=0, last=-1):
        self._abspath = abspath
        self.mimetype = mimetypes.guess_type(abspath)[0]
        self.length = os.path.getsize(abspath)
        self.chunked = chunked
        self.begin = begin
        self.last = last

    # return the bytes of the selected part of the file
    # Others: The range is inclusive in the request but not in python, so we need to add 1...
    def toBytes(self):
        try:
            file = open(self._abspath, 'rb')
            if self.chunked:
            
                if self.begin == '': # bytes=-500 The last 500 bytes
                    print(file.seek(-1*(int(self.last) + 1), 2))
                    return file.read()
                else: 
                    file.seek(self.begin)
                    if self.last == '': # bytes=9500- read from the 9500th byte
                        return file.read()
                    else:
                        return file.read(int(self.last) + 1 - int(self.begin)) # bytes=9500-10000 read from the 9500th byte to the 10000th byte
            else:
                return file.read()
        except Exception:
            return b''