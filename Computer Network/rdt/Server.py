from rdt import socket

if __name__ == "__main__":
    try:
        server_socket = socket()
        server_socket.bind(('127.0.0.1', 63000))
        server_socket.accpet()
        while True:
            data = server_socket.recv()
            print("receive", data)
            server_socket.send(data)
    except KeyboardInterrupt:
        pass