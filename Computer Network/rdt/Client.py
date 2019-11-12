from rdt import socket

if __name__ == "__main__":
    client_socket = socket()
    client_socket.bind(('', 12345))
    client_socket.connect(('127.0.0.1', 63000))


    #################
    # Original Test #
    #################
    # MESSAGE = "TEST_MESSAGE_中文_TEST_MESSAGE"
    # client_socket.send(MESSAGE)
    # data = client_socket.recv()
    # assert data == MESSAGE


    #########################
    # Manually sending test #
    #########################
    while True:
        MESSAGE = input('input:')
        client_socket.send(MESSAGE)
        data = client_socket.recv()
        print("server:",data)
    


    ###################
    # large text test #
    ###################
    # fp = open('C:\\Users\\ASUS\\desktop\\alice.txt', 'r')
    # MESSAGE = fp.read()
    # fp.close()
    # client_socket.send(MESSAGE)
    # data = client_socket.recv()
    # if(data == MESSAGE):
    #     print("SAME!!!!")
    # else:
    #     print("WRONG!!!")
