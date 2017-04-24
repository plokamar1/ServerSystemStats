import socket

class SocketObj:
    def __init__(self, sock= None):
        if sock == None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, SE_host, SE_port):
        self.s.connect( (SE_host, SE_port))
        print('connected to server')

    def send_to_server(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.s.send((msg[totalsent:]))
            if sent == 0:
                raise RuntimeError("Socket disconnected")
            totalsent += sent
        print('Message sent')

