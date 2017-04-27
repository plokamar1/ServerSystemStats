import socket
import sys
from systemFunctions import *

class Connection:
    def __init__(self, sock=None):
        if sock == None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, SE_host, SE_port):
        try:
            self.s.connect((SE_host, SE_port))
            print('connected to server\n')
        except ConnectionRefusedError:
            print('The server refused connection\n')
            sys.exit(0)

    def send_to_server(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.s.send((msg[totalsent:].encode(
                encoding='UTF-8', errors='strict')))
            if sent == 0:
                raise RuntimeError("Socket disconnected")
                sys.exit(0)
            totalsent += sent
        print('Message sent')

    def connect_and_send(self, SE_host, SE_port, client_name):
        self.connect_to_server(SE_host, SE_port)
        msg = json.dumps(vars(ServerStatusObj(client_name)), sort_keys=True, indent=4)
        self.send_to_server(msg)
