import socket
import os
from configparser import SafeConfigParser
from networkFunctions import *

if __name__ == "__main__":
    config = SafeConfigParser()
    if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + '\config.ini'):
        config.read(os.path.dirname(os.path.realpath(__file__)) + '\config.ini')
        config.sections()

        se_port = config.getint('Settings','Server_port')
        se_buffer = config.getint('Settings','Buffer_size')
        se_host = config.get('Settings','Host_address')

        connObj = SocketObj()
        connObj.server_bind(se_host,se_port)
        connObj.server_listen()
        connObj.server_receive(se_buffer)