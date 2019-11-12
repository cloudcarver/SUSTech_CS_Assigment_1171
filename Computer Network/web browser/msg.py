import config
import os
import urllib.parse
import http.cookies
from BrowerPage import *
from FileResponse import *

class RequestDecoder(object):

    def __init__(self, inputBytes):
        self.request_list = inputBytes.decode().split('\r\n')
        self.itemdict = {}
        self.cookie = http.cookies.SimpleCookie()
        

    def decode(self):
        # The first line contains request method, parameter and protocol and its version
        first_line_list = self.request_list[0].split(' ')
        
        if len(first_line_list) < 3:
            return False

        self.itemdict["method"] = first_line_list[0]
        self.itemdict["param"] = first_line_list[1]
        self.itemdict["protocol"] = first_line_list[2]
        self.itemdict["Range"] = False

        # Store the other lines in itemdict
        for i in range(1, len(self.request_list)):
            kvlist = self.request_list[i].split(":", 1)
            if len(kvlist) != 2:
                continue

            if kvlist[0] == "Cookie":
                self.cookie.load(kvlist[1])
                continue
            
            self.itemdict[kvlist[0]] = kvlist[1]

        return True

class Response(object):

    OK = 'OK'
    METHOD_NOT_ALLOWED = 'METHOD_NOT_ALLOWED'
    HEAD = 'HEAD'
    GET = 'GET'

    def __init__(self, request):
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.request = request
        self.path = urllib.parse.unquote(request.itemdict["param"])
        self.method = request.itemdict["method"]

    # def _http_header_206(self):
    #     return [
    #         b'HTTP/1.1 206 Partial Content\r\n', 
    #         b'Connection: Keep-Alive\r\n',
    #         b'Accept-Ranges: bytes\r\n'
    #     ]

    def _error_405(self):
        return [
            b'HTTP/1.1 405 Method Not Allowed\r\n', 
            b'Content-Type:text/html; charset=utf-8\r\n', 
            b'Connection: Keep-Alive\r\n', 
            b'\r\n',
            b'<html>\r\n', 
            b'<head><title>Web file browser</title></head>\r\n',  
            b'<pre>\r\n', 
            b'<body bgcolor = "white">\r\n', 
            b'<h1>Error 405 : Method Now Allowed</h1>',
            b'</body></html>\r\n', 
            b'\r\n'
        ]

    def _error_404(self):
        return [
            b'HTTP/1.1 404 Object Not Found\r\n', 
            b'Content-Type:text/html; charset=utf-8\r\n', 
            b'Connection: Keep-Alive\r\n', 
            b'\r\n',
            b'<html>\r\n', 
            b'<head><title>Web file browser</title></head>\r\n',  
            b'<pre>\r\n', 
            b'<body bgcolor = "white">\r\n', 
            b'<h1>Error 404 : Object Not Found</h1>',
            b'</body></html>\r\n', 
            b'\r\n'
        ]

    def _redir_302(self, location):
        return [
            b'HTTP/1.1 302 Found\r\n', 
            b'Connection: Keep-Alive\r\n', 
            'Location: {}'.format(location).encode(),
            b'\r\n',
        ]
    
    def html_len(self, htmlList):
        cnt = 0
        for line in htmlList:
            cnt += len(line)
        return cnt

    def validate_path(self):
        if self.method != Response.GET and self.method != Response.HEAD:
            return Response.METHOD_NOT_ALLOWED
        else:
            return Response.OK

    def toHttpResponse(self):
        validation_result = self.validate_path()
        if validation_result != Response.OK:
            if validation_result == Response.METHOD_NOT_ALLOWED:
                return self._error_405()
            else:
                return self._error_404()

        rtn = [
                b'HTTP/1.0 200 OK\r\n', 
                b'Accept-Ranges: bytes\r\n',
                b'Connection: close\r\n'
                ] if config.HTTP == 1.0 else[
                b'HTTP/1.1 200 OK\r\n', 
                b'Accept-Ranges: bytes\r\n',
                b'Connection: Keep-Alive\r\n'
            ]

        # OK. 
        if self.path == '/root/':
            path = '/'
        else:
            path = self.path

        if os.path.isdir(self.root + path): #return browser page
            # redirect if the user access the root directory and there are some contents in the cookie
            if (self.path == '/') and ("lastdir" in self.request.cookie) and (self.request.cookie["lastdir"].value != '/'):# The browser is visting root dir
                print("redirect to",self.request.cookie["lastdir"].value)
                return self._redir_302(self.request.cookie["lastdir"].value)
            
            htmlpage_bytes = BrowserPage(self.root, path).toHtml()

            # Set Cookie to remember the last dir
            rtn += [
                'Set-Cookie: lastdir={};Path=/\r\n'.format(urllib.parse.quote(path)).encode()
            ]
            print("Set cookie : {}".format(urllib.parse.quote(path)))

            # Content Type and Content Length
            rtn += [
                b'Content-Type:text/html; charset=utf-8\r\n',
                'Content-Length:{}\r\n'.format(self.html_len(htmlpage_bytes)).encode(),
                b'\r\n'
            ]

            if self.method != Response.HEAD:
                rtn = rtn + htmlpage_bytes
                rtn.append(b'\r\n')
            return rtn
        else: # return file

            if not self.request.itemdict["Range"]: # There is no range request contained in the request 

                file_bytes = FileResponse(self.root + self.path)
                rtn += [
                    'Content-Type:{}\r\n'.format(file_bytes.mimetype).encode(),
                    'Content-Length:{}\r\n'.format(file_bytes.length).encode(),
                    b'\r\n'
                ]

                if self.method != Response.HEAD:
                    rtn.append(file_bytes.toBytes())
                    rtn.append(b'\r\n')
            
            else: # YO DWANG, A troublesome client send me a range request. 
                rtn = [
                    b'HTTP/1.1 206 Partial Content\r\n', 
                    b'Accept-Ranges: bytes\r\n',
                    b'Connection: Keep-Alive\r\n'
                ]
                range_list = Util.range_handler(self.request.itemdict["Range"])

                # multi_ranges = len(range_list) > 1

                ###

                # Guess what? I don't need to write this shit anymore. Fking multi-ranges

                # if multi_ranges:
                #     if self.method != Response.HEAD:
                #         rtn += [
                #             'Content-Type: multipart/byteranges; boundary=THIS_STRING_SEPARATES\r\n'.encode(),
                #             b'\r\n',
                #             b'THIS_STRING_SEPARATES', 
                #             b'\r\n'
                #         ]

                #     for element in range_list:
                #         file_bytes = FileResponse(self.root + self.path, chunked=True, begin=element[0], last=element[1])
                #         if self.method != Response.HEAD:
                #             rtn += [
                #                 'Content-Type: {}\r\n'.format(file_bytes.mimetype).encode(),
                #                 'Content-Range: bytes {}-{}/{}\r\n'.format(element[0], element[1], '*').encode(),
                #                 b'\r\n'
                #             ]
                #             rtn.append(file_bytes.toBytes())
                #             rtn += [
                #                 b'THIS_STRING_SEPARATES', 
                #                 b'\r\n']
                # else:

                # Only care about the first range no whether how many ranges are requested.

                first_range = range_list[0]

                file_bytes = FileResponse(self.root + self.path, chunked=True, begin=first_range[0], last=first_range[1])

                whole_file = FileResponse(self.root + self.path)

                rtn += [
                    'Content-Range: bytes {}-{}/{}\r\n'.format(first_range[0], first_range[1], whole_file.length).encode(),
                    'Content-Type:{}\r\n'.format(file_bytes.mimetype).encode(),
                    'Content-Length:{}\r\n'.format(file_bytes.length).encode(),
                    b'\r\n'
                ]
                if self.method != Response.HEAD:
                    rtn.append(file_bytes.toBytes())
                
                if self.method != Response.HEAD:
                    rtn.append(b'\r\n')
            
            return rtn

class Util():
    @staticmethod
    def range_handler(range_request):
        rtn = []
        range_list = range_request.split(';')
        for ran in range_list:
            if ran == '':
                continue
            ran = ran.split('=')[1]
            ran = ran.split('-')
            rtn.append([Util.int_else_empty(ran[0]), Util.int_else_empty(ran[1])])

        return rtn

    @staticmethod
    def int_else_empty(param):
        if param != '':
            return int(param)
        else:
            return param

if __name__ == "__main__":
    range_list = Util.range_handler("bytes=-500;")
    print(len(range_list))

        

    
        

