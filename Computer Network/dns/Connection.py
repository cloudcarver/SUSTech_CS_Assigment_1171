from socket import *

class UDPConnection(object):

    UDP_RECV_BUF = 2048

    def __init__(self,  VERBOSE):
        self.VERBOSE = VERBOSE
        self.socket = socket(AF_INET, SOCK_DGRAM)
            
    def bind(self, addr, port):
        self.port = port
        self.socket.bind((addr, self.port))
        if self.VERBOSE:
            print("UDP connection is set up.")

    # Receive the message from the client side in blocked way
    def blocked_recv(self):
        message, self.address = self.socket.recvfrom(self.UDP_RECV_BUF)
        if self.VERBOSE:
            print("Receive {} bytes from {}".format(len(message), self.address))
        return message
    
    # Send the message to specified server
    def sendto_server(self, msg, addr, port):
        if self.VERBOSE:
            print("Send {} bytes to {}:{}".format(len(msg), addr, port))
        self.socket.sendto(msg, (addr, port))

    # Send the message to the client
    def sendto(self, msg):
        if self.VERBOSE:
            print("Send {} bytes to {}".format(len(msg), self.address))
        self.socket.sendto(msg, self.address)