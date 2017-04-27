class Helper:
    def __init__(self):
        self.read_config()
    #This function returns a dictionary with the settings the user
    #wrote in config.ini

    def read_config(self):
        import platform
        import os
        import sys
        from configparser import SafeConfigParser
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
                if config.has_section('Settings'):
                    se_port = config.getint('Settings', 'Server_port')
                    se_buffer = config.getint('Settings', 'Buffer_size')
                    se_host = config.get('Settings', 'Host_address')
                    se_mongo_host = config.get('Settings', 'Mongo_Client_host')
                    se_mongo_port = config.getint(
                        'Settings', 'Mongo_Client_port')
                    config_sets = {'SE_port': se_port,
                                   'SE_buffer': se_buffer,
                                   'SE_host': se_host,
                                   'SE_mongo_host': se_mongo_host,
                                   'SE_mongo_port': se_mongo_port
                                   }
                    return config_sets
                else:
                    print(
                        '[Settings] section or [Server] section missing from config.ini')
                    sys.exit(0)
            else:
                print('Config file not found.\n')
                configPath = input(
                    'Please paste here the exact directory of config.ini.(C://config.ini)\n')

    def set_client_name(self, config_sets):
        import socket
        if config_sets['client_name'] == 'default':
            config_sets['client_name'] = socket.gethostname()
        return config_sets

    #got this code from rominf in stack overflow
    #It checks if a library is installed. If not the function downloads it
    #and imports it
    def install_package(self, package):
        import importlib
        try:
            importlib.import_module(package)
        except ImportError:
            import pip
            pip.main(['install', package])
