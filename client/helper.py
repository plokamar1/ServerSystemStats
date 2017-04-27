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
                    print('[Settings] section or [Server] section missing from config.ini')
                    sys.exit(0)
            else:
                print('Config file not found.\n')
                configPath = input('Please paste here the exact directory of config.ini.(C://config.ini)\n')

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

