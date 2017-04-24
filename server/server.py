import socket
import os
from configparser import SafeConfigParser
from networkFunctions import *

if __name__ == "__main__":
    config = SafeConfigParser()
    if os.path.isfile(os.getcwd() + '\server\config.ini'):
        config.read(os.getcwd() + '\server\config.ini')
        config.sections()

        se_port = config.getint('Settings','Server_port')
        se_buffer = config.getint('Settings','Buffer_size')
        connObj = SocketObj()
        connObj.server_bind(se_port)
        connObj.server_listen()
        connObj.server_receive(se_buffer)