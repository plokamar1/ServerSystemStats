if __name__ == "__main__":
    from helper import *
    helperObj = Helper()
    packages = ['psutil','socket','configparser','json','pymongo']
    for package in packages:
        helperObj.install_package(package)
    config_sets = helperObj.read_config()

    from networkFunctions import *
    from databaseFunctions import *
    connObj = SocketObj()
    connObj.server_bind(config_sets['SE_host'], config_sets['SE_port'])
    connObj.server_listen()
    while 1:
        data = connObj.server_receive(config_sets['SE_buffer'])
        insert_post(data, config_sets['SE_mongo_host'], config_sets['SE_mongo_port'])
