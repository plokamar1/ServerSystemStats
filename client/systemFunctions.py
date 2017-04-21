import psutil, json, string, time, platform
import os

class diskObj:
    def __init__(self,partitions_stats):
        self.partitions_stats = partitions_stats


class cpuObj:
    def __init__(self,loadAverage,percentPerCpu):
        self.loadAverage = {"oneMinute":loadAverage[0],"fiveMinutes":loadAverage[1],"fifteenMinutes":loadAverage[2]}
        self.currentUsagePerCore = percentPerCpu



def CPUStats():
    #If the OS is not windows get load average
    if platform.system() != 'Windows':
        loadAverage = os.getloadavg()
    else:
        loadAverage = [None,None,None]

    #Get current cpu usage
    percentPerCpu = psutil.cpu_percent(interval=1, percpu=True)

    #Construct the cpu object
    coreObj = cpuObj(loadAverage,percentPerCpu)
    cpuJSON = json.dumps(vars(coreObj),sort_keys=True, indent=4)

    return cpuJSON


def DISKStats():
    partitions_stats = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            diskUsage = psutil.disk_usage(partition.mountpoint)
            diskUsage_gb = ('%.2f' % (diskUsage.used/1073741824)) + " Gb"
            diskIO = psutil.disk_io_counters()

            #Creating the dictionary for each partition
            eachPart_stats = { 
                "Name": partition.mountpoint, 
                "usagePercent":diskUsage.percent, 
                "usageGB":diskUsage_gb, 
                "read_count": diskIO.read_count, 
                "write_count":diskIO.write_count
                }
            #Put each dictionary to this list
            partitions_stats.append(eachPart_stats)
        except OSError as e:
            print("No permissions for disk: "+partition.mountpoint+"\n")

    partObject = diskObj(partitions_stats)
    diskJSON = json.dumps(vars(partObject),sort_keys=True, indent=4)

    return diskJSON

DISKStats()
CPUStats()