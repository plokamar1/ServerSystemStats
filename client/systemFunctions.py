import psutil
import json
import string
import time
import platform
import os
import time

class ServerStatusObj:
    def __init__(self, diskStatusObj, cpuStatusObj, portsStatus, ramStatus, current_time):
        self.DiskStatus = diskStatusObj
        self.CpuStatus = cpuStatusObj
        self.PortsStatus = portsStatus
        self.RamStatus = ramStatus
        self.time = current_time

class DiskObj:
    def __init__(self, partitions_stats):
        self.partitions_stats = partitions_stats


class CpuObj:
    def __init__(self, loadAverage, percentPerCpu):
        self.loadAverage = {
            "oneMinute": loadAverage[0], "fiveMinutes": loadAverage[1], "fifteenMinutes": loadAverage[2]}
        self.currentUsagePerCore = percentPerCpu

class ConnPorts:
    def __init__(self, name):
        self.port_name = name
        self.connections = 1

    def add_connection(self):
        self.connections += 1

class RamObj:
    def __init__(self,ramStatus_percent,ramStatus_total,ramStatus_available,ramStatus_cached,ramStatus_used):
        self.total = ramStatus_total
        self.percent = ramStatus_percent
        self.available = ramStatus_available
        self.cached = ramStatus_cached
        self.used = ramStatus_used


def get_cpu_stats():
    #If the OS is not windows get load average
    if platform.system() != 'Windows':
        loadAverage = os.getloadavg()
    else:
        loadAverage = [None, None, None]

    #Get current cpu usage
    percentPerCpu = psutil.cpu_percent(interval=1, percpu=True)
    #Construct the cpu object
    coreObj = CpuObj(loadAverage, percentPerCpu)
    #cpuJSON = json.dumps(vars(coreObj), sort_keys=True, indent=4)

    return coreObj


def get_disk_stats():
    partitions_stats = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            diskUsage = psutil.disk_usage(partition.mountpoint)
            diskUsage_gb = ('%.2f' % (diskUsage.used / 1073741824)) + " Gb"
            diskTotal_gb = ('%.2f' % (diskUsage.total / 1073741824)) + " Gb"
            diskIO = psutil.disk_io_counters()
            #Creating the dictionary for each partition
            eachPart_stats = {
                "Name": partition.mountpoint,
                "Total": diskTotal_gb,
                "usagePercent": diskUsage.percent,
                "usageGB": diskUsage_gb,
                "read_count": diskIO.read_count,
                "write_count": diskIO.write_count
            }
            #Put each dictionary to this list
            partitions_stats.append(eachPart_stats)
        except OSError as e:
            print("No permissions for disk: " + partition.mountpoint + "\n")

    partObject = DiskObj(partitions_stats)
    #diskJSON = json.dumps(vars(partObject), sort_keys=True, indent=4)

    return partObject

# def get_dict(connObjects):
#     return connObjects.__dict__


def get_connections():
    retStr = ""
    i = 0
    ports = []
    connObjects = []
    connList = []
    for connection in psutil.net_connections():
        if connection.status == 'ESTABLISHED':
            if connection.raddr[1] not in ports:
                ports.append(connection.raddr[1])
                connObjects.append(ConnPorts(connection.raddr[1]))

    for obj in connObjects:
        for connection in psutil.net_connections():
            if connection.status == 'ESTABLISHED' and connection.raddr[1] == obj.port_name:
                obj.add_connection()
        
        connList.append(vars(obj))
    #print(connList)
    #connsJSON = json.dumps(connObjects, default=get_dict)
    return connList

def get_ram_status():
    ramStatus = psutil.virtual_memory()
    ramStatus_percent = ramStatus.percent
    ramStatus_total = ('%.2f' % (ramStatus.total / 1073741824)) + " Gb"
    ramStatus_available = ('%.2f' % (ramStatus.available / 1073741824)) + " Gb"
    ramStatus_used = ('%.2f' % (ramStatus.used / 1073741824)) + " Gb"
    if platform.system() != 'Windows':
        ramStatus_cached = ('%.2f' % (ramStatus.cached / 1073741824)) + " Gb"
    else:
        ramStatus_cached = None

    ramObj = RamObj( ramStatus_percent,ramStatus_total,ramStatus_available,ramStatus_cached,ramStatus_used)

    return ramObj


def get_system_stats():
    partObject = get_disk_stats()
    coreObj = get_cpu_stats()
    ramObj = get_ram_status()
    connections = get_connections()
    current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    serverObj = ServerStatusObj( vars(partObject), vars(coreObj),connections,vars(ramObj), current_time)
    fp = open('test.json','w')
    fp.write(json.dumps(vars(serverObj), sort_keys=True, indent=4))
    print(json.dumps(vars(serverObj), sort_keys=True, indent=4))
    return(json.dumps(vars(serverObj), sort_keys=True, indent=4))



#print( vars(get_disk_stats()))
#print(get_cpu_stats())
#call_them_all()
#get_system_stats()
#get_system_stats()