#libraries import
import time
import json
import os
import platform
from configparser import SafeConfigParser

#scripts import
from systemFunctions import *
from networkFunctions import *

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
    install_and_import('psutil')
    install_and_import('socket')
    install_and_import('configparser')

    #Checking the OS because the syntax is different
    if platform.system() == 'Windows':
        fl = '\config.ini'
    else:
        fl = '/config.ini'
    
    configPath = os.path.dirname(os.path.realpath(__file__)) + fl

    while 1:
        if os.path.isfile(configPath):
            config = SafeConfigParser()
            config.read(configPath)
            print(configPath)
            config.sections()

            sleep_time = config.getint('Settings', 'Get_Status_Every')
            client_name = config.get('Settings', 'Client_Name')
            server_host = config.get('Server', 'Server_host')
            server_port = config.getint('Server', 'Port')

            if client_name == 'default':
                client_name = socket.gethostname()

            connObj = SocketObj()
            
            i = 1
            while 1:
                connObj = SocketObj()
                connObj.connect_to_server(server_host, server_port)
                msg = get_system_stats(client_name)
                connObj.send_to_server(msg)
                time.sleep(sleep_time)
        else:
            print('Config file not found.\n')
            configPath = input('Please paste here the exact directory of config.ini.(C://config.ini)\n')
