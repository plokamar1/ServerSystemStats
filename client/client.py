#libraries import
import psutil, time, json, os
from configparser import SafeConfigParser

#scripts import
from systemFunctions import *
from networkFunctions import *

#got this code from rominf in stack overflow
def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

install_and_import('transliterate')

if __name__ == "__main__":
    install_and_import('psutil')
    install_and_import('daemon')
    config = SafeConfigParser()
    if os.path.isfile(os.getcwd()+'\client\config.ini'):
        print(config.read(os.getcwd()+'\client\config.ini'))
        print(config.sections())
        sleep_time = config.getint('Settings','Get_Status_Every')

    # while ( i>0 ):
    #     print(CPUStats())
    #     time.sleep(30)
