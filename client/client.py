#libraries import
import time
import json
import os
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
    finally:
        globals()[package] = importlib.import_module(package)


if __name__ == "__main__":

    install_and_import('psutil')
    install_and_import('socket')

    config = SafeConfigParser()
    if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + '\config.ini'):
        config.read(os.path.dirname(os.path.realpath(__file__)) + '\config.ini')
        config.sections()

        sleep_time = config.getint('Settings', 'Get_Status_Every')
        server_host = config.get('Server', 'Server_host')
        server_port = config.getint('Server', 'Port')

        connObj = SocketObj()
        connObj.connect_to_server(server_host, server_port)
        i = 1
        while (i>0):
            msg = get_system_stats()
            connObj.send_to_server(msg)
            time.sleep(sleep_time*60)
