#scripts import
if __name__ == "__main__":
    from helper import *
    helperObj = Helper()
    packages = ['psutil','socket','configparser','json']
    for package in packages:
        helperObj.install_package(package)
    config_sets = helperObj.read_config()
    config_sets = helperObj.set_client_name(config_sets)

    from systemFunctions import *
    from networkFunctions import *
    while 1:
        connObj = Connection()
        connObj.connect_and_send(config_sets['server_host'], config_sets['server_port'], config_sets['client_name'])
        time.sleep(config_sets['sleep_time'])
