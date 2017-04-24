import socket


class SocketObj:
    def __init__(self, sock=None):
        if sock == None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, SE_host, SE_port):
        self.s.connect((SE_host, SE_port))
        print('connected to server')

    def server_bind(self, host, port):
        self.s.bind((host, port))
        print('Binded to port: ' + str(port))

    def server_listen(self):
        self.s.listen(1)
        print('Listening...')

    def server_receive(self, buffer_size):
        conn, addr = self.s.accept()
        print(addr)
        while 1:
            data = conn.recv(buffer_size)
            if not data:
                break
            print(data.decode())
        conn.close()

    def send_to_server(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.s.send((msg[totalsent:].decode(
                encoding='UTF-8', errors='strict')))
            if sent == 0:
                raise RuntimeError("Socket disconnected")
            totalsent += sent
        print('Message sent')
