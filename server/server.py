import socket
import os
import platform
from configparser import SafeConfigParser
from networkFunctions import *

if __name__ == "__main__":
    config = SafeConfigParser()

    if platform.system() == 'Windows':
        fl = '\config.ini'
    else:
        fl = '/config.ini'
    if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + fl):
        config.read(os.path.dirname(os.path.realpath(__file__)) + fl)
        config.sections()

        se_port = config.getint('Settings', 'Server_port')
        se_buffer = config.getint('Settings', 'Buffer_size')
        se_host = config.get('Settings', 'Host_address')

        connObj = SocketObj()
        connObj.server_bind(se_host, se_port)
        connObj.server_listen()
        connObj.server_receive(se_buffer)
    else:
        print('Config file not found')
