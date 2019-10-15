from socket import *
import Config
import time

class UDPConnection(object):

    UDP_RECV_BUF = 2048

    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
            
    def bind(self, addr, port):
        self.port = port
        self.socket.bind((addr, self.port))
        if Config.VERBOSE:
            print("UDP connection is set up.")

    # Receive the message from the client side in blocked way
    def blocked_recv(self):
        try:
            message, self.address = self.socket.recvfrom(self.UDP_RECV_BUF)
            if Config.VERBOSE:
                print("Receive {} bytes from {}".format(len(message), self.address))
            if Config.DEBUG:
                print("Received Message:{}".format(message))
        except ConnectionResetError: # Wait and try again if the server close the connection. Because the server treat frequent requests as attack.
            time.sleep(10)
            if Config.VERBOSE:
                print("Too frequent connection, try again...")
            return self.blocked_recv()
        
        return message
    
    # Send the message to specified server
    def sendto_server(self, msg, addr, port):
        if Config.VERBOSE:
            print("Sending {} bytes to {}:{}".format(len(msg), addr, port))
        self.socket.sendto(msg, (addr, port))
        if Config.DEBUG:
            print("Message Sent:{}".format(msg))
        

    # Send the message to the client
    def sendto(self, msg):
        if Config.VERBOSE:
            print("Sending {} bytes to {}".format(len(msg), self.address))
        self.socket.sendto(msg, self.address)
        if Config.DEBUG:
            print("Message Sent:{}".format(msg))
        