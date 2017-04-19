#libraries import
import psutil, time, json, os
from configparser import SafeConfigParser
#scripts import
from systemFunctions import *
from networkFunctions import *


config = SafeConfigParser()
if os.path.isfile(os.getcwd()+'\client\config.ini'):
    print(config.read(os.getcwd()+'\client\config.ini'))
    print(config.sections())
    get_data = config.getint('Settings','Get_Status_Every')
    print(get_data)


if __name__ == "__main__":
    if os.path.isfile(os.getcwd()+'\config.ini'):
        print('Its here')
    # i = 1
    # while ( i>0 ):
    #     print(CPUStats())
    #     time.sleep(30)
    i=0