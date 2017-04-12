#libraries import
import psutil, time, json

#scripts import
from systemFunctions import *


if __name__ == "__main__":
    i = 1
    while ( i>0 ):
        print(CPUStats())
        time.sleep(30)