#libraries import
import time, json, os
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
    if os.path.isfile(os.getcwd()+'\client\config.ini'):
        config.read(os.getcwd()+'\client\config.ini')
        config.sections()
        sleep_time = config.getint('Settings','Get_Status_Every')
        server_ip = config.get('Server', 'Server_IP')
        server_port = config.getint('Server', 'Port')
        
        print(sleep_time)
        print(server_ip)
        print(server_port)

    # while ( i>0 ):
    #     print(CPUStats())
    #     time.sleep(30)
