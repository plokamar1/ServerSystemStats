import socket
import os
import platform
from configparser import SafeConfigParser
from networkFunctions import *
from databaseFunctions import *

#got this code from rominf in stack overflow
#It checks if a library is installed. If not the function downloads it
#and imports it
def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
        print(package + ' was installed!')
    finally:
        globals()[package] = importlib.import_module(package)

if __name__ == "__main__":
    install_and_import('configparser')
    install_and_import('pymongo')
    install_and_import('json')
    
    config = SafeConfigParser()

    if platform.system() == 'Windows':
        fl = '\config.ini'
    else:
        fl = '/config.ini'

    configPath = os.path.dirname(os.path.realpath(__file__)) + fl
    while 1:
        if os.path.isfile(configPath):
            config = SafeConfigParser()
            config.read(configPath)
            config.sections()
            #Getting the configurations
            se_port = config.getint('Settings', 'Server_port')
            se_buffer = config.getint('Settings', 'Buffer_size')
            se_host = config.get('Settings', 'Host_address')
            se_mongo_host = config.get('Settings','Mongo_Client_host')
            se_mongo_port = config.getint('Settings','Mongo_Client_port')

            connObj = SocketObj()
            connObj.server_bind(se_host, se_port)
            connObj.server_listen()
            while 1:
                data = connObj.server_receive(se_buffer)
                data = json.loads(data)
                insert_post(data,se_mongo_host,se_mongo_port)
        else:
            print('Config file not found')
            configPath = input('Please paste here the exact directory of config.ini.(C://config.ini)\n')
