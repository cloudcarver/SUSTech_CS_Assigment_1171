import os
import urllib

# Just consider this is a JavaScript file for dymaically contructing web pages
class BrowserPage(object):
    def __init__(self, root, path):
        self._root = root
        self._path = path

    # def changePath(self, param):
    #     self._path = param

    # HTML header
    def _header(self):
        return [
            b'<html>\r\n', 
            b'<head><title>Web file browser</title></head>\r\n',  
            b'<pre>\r\n', 
            b'<body bgcolor = "white">\r\n', 
            b'<font size="6" color = "grey" face="consalas">Web </font>',
            b'<font size="6" color = "#FFB90F" face="consalas">File Browser</font><br />\r\n',
            b'<hr>\r\n'
        ]

    # HTML footer
    def _footer(self):
        return [
            b'</pre>\r\n', 
            b'<hr>\r\n', 
            b'</body></html>\r\n'
        ]

    # HTML body
    def _body(self):

        def getLastDir(path):
            rtn = "/"
            tmp_list = path.split('/')
            for i in range(0, len(tmp_list) - 1):
                if tmp_list[i] == '':
                    continue
                rtn += tmp_list[i] + ("/"  if( i != (len(tmp_list) - 2) and tmp_list[i] != '') else "")
            return rtn if rtn != '/' else '/root/'

        # The path is not valid, then
        if not os.path.exists(self._root + self._path):
            return [
                b'<p>Path not found.</p>'
            ]



        # The parent directory
        line = '<a href = {}><font size = 5>{}</font></a><br />'
        rtn = []
        rtn.append(line.format(urllib.parse.quote(getLastDir(self._path)), '..').encode())

        dir_list = os.listdir(self._root + "/" + self._path)
        for element in dir_list:
            separator = "/" if self._path != "/" else ""
            rtn.append(line.format(urllib.parse.quote(self._path + separator + element), element).encode())

        return rtn

    def toHtml(self):
        return self._header() + self._body() + self._footer()