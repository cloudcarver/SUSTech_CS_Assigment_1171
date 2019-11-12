
from socket import *
import config
import time

class TCPConnection(object):

    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.bind(config.HOST, config.PORT)

    def bind(self, addr, port):
        self.socket.bind((addr, port))
        self.socket.listen(10)
        if config.DEBUG:
            print("TCP server on. {}:{}".format(addr, port))

    def blocked_recv(self):
        connection, client_addr = self.socket.accept()
        if config.DEBUG:
            print("Connection bulit. Client: {}".format(client_addr))
        return connection