import asyncio
import config
import threading
from Connection import *
from msg import *

RUN = True

class client_thread(threading.Thread):

    # The maximum bytes can be buffered in a single TCP request
    MAX_BUF = 2048

    def __init__(self, threadName, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.threadName = threadName
    
    # re-implement the run method in the threading class
    def run(self):
        # Receive data
        data = self.conn.recv(client_thread.MAX_BUF) 
        # Handle data
        self.handleData(data) 
        self.conn.close() 

    def handleData(self, data):
        global RUN
        if data == '':
            return 0

        # Contruct a meaningful message dictory from the byte stream by a decoder
        requestDecoder = RequestDecoder(data)

        if not requestDecoder.decode():#If the data is some meaningless data like '\r\n', just simple ignore it
            return 0

        # The reponse object we get after decoding
        response = Response(requestDecoder)

        # A list of bytes we need to send to the client. Could be a web page or a file
        rtnList = response.toHttpResponse()
        
        for line in rtnList:
            if RUN:

                # If the client don't want to connect to us, just let it be.
                try:
                    # Send a line of data to the client
                    self.conn.send(line)
                except ConnectionAbortedError:
                    if config.VERBOSE:
                        print("A connection is aborted by the client side.")
                    break
                except ConnectionResetError:
                    if config.VERBOSE:
                        print("A connection is aborted by the client side.")
                    break
                if config.DEBUG:
                    print(line)
            else:
                break
        

# This is the thread for receiving command from the console.
# There are only two commands available for now : quit and exit
class control_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global RUN
        while RUN:
            command = input(">")
            if command == "exit" or command == "quit":
                print("Closing server...")
                RUN = False
            else:
                print("Invalid command.")


# A classic framework to deal with concurrent requests by multi-threading.
def run_multithreading_server():
    global RUN
    # The server socket
    tcpConnection = TCPConnection()
    threadCnt = 0
    # Start the control thread
    control_thread().start()
    while RUN:
        # Listen carefully! If there is someone knocking on our door, bring him(it is better a 'her') in!
        clientConnectionSocket = tcpConnection.blocked_recv()
        # Start the thread and continue to listen for a new connecting request
        client_thread("Thread {}".format(threadCnt), clientConnectionSocket).start()
        threadCnt += 1

if __name__ == '__main__':
    run_multithreading_server()
