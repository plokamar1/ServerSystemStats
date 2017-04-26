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

#This function returns a dictionary with the settings the user
#wrote in config.ini


def read_config(configPath):
    config = SafeConfigParser()
    config.read(configPath)
    config.sections()
    if config.has_section('Settings') and config.has_section('Server'):
        sleep_time = config.getint('Settings', 'Get_Status_Every')
        client_name = config.get('Settings', 'Client_Name')
        server_host = config.get('Server', 'Server_host')
        server_port = config.getint('Server', 'Port')
        config_sets = {'sleep_time': sleep_time,
                    'client_name': client_name,
                    'server_host': server_host,
                    'server_port': server_port
                    }
        return config_sets
    else:
        return False


if __name__ == "__main__":
    install_and_import('psutil')
    install_and_import('socket')
    install_and_import('configparser')

    #Checking the OS because the syntax of the directories is different
    if platform.system() == 'Windows':
        fl = '\config.ini'
    else:
        fl = '/config.ini'

    configPath = os.path.dirname(os.path.realpath(__file__)) + fl
    while 1:
        if os.path.isfile(configPath):
            config_sets = read_config(configPath)
            if not config_sets:
                print('[Settings] section or [Server] section missing from config.ini')
                break

            if config_sets['client_name'] == 'default':
                config_sets['client_name'] = socket.gethostname()

            connObj = SocketObj()
            while 1:
                connObj = SocketObj()
                connObj.connect_to_server(
                    config_sets['server_host'], config_sets['server_port'])
                msg = get_system_stats(config_sets['client_name'])
                connObj.send_to_server(msg)
                time.sleep(config_sets['sleep_time'])
        else:
            print('Config file not found.\n')
            configPath = input(
                'Please paste here the exact directory of config.ini.(C://config.ini)\n')
