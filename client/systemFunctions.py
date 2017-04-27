import psutil
import json
import string
import platform
import os
import time


class ServerStatusObj:
    def __init__(self, client_name):
        self.ClientName = client_name
        self.get_cpu_stats()
        self.get_disk_stats()
        self.get_ram_stats()
        self.get_time_dct()
        self.get_connections()

    def get_cpu_stats(self):
        #If the OS is not windows get load average
        if platform.system() != 'Windows':
            loadAverage = os.getloadavg()
        else:
            loadAverage = [None, None, None]

        loadAverageLst = {
            "oneMinute": loadAverage[0],
            "fiveMinutes": loadAverage[1],
            "fifteenMinutes": loadAverage[2]
        }

        percentPerCpu = psutil.cpu_percent(interval=1, percpu=True)
        self.CpuStatus = {
            "currentUsagePerCore": percentPerCpu,
            "loadAverage": loadAverageLst
        }

    def get_disk_stats(self):
        partitions_stats = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                diskUsage = psutil.disk_usage(partition.mountpoint)
                diskUsage_gb = ('%.2f' % (diskUsage.used / 1073741824)) + " Gb"
                diskTotal_gb = ('%.2f' %
                                (diskUsage.total / 1073741824)) + " Gb"
                diskIO = psutil.disk_io_counters()
                #Creating the dictionary for each partition
                eachPart_stats = {
                    "name": partition.mountpoint,
                    "total": diskTotal_gb,
                    "usagePercent": diskUsage.percent,
                    "usageGB": diskUsage_gb,
                    "read_count": diskIO.read_count,
                    "write_count": diskIO.write_count
                }
                #Put each dictionary to this list
                partitions_stats.append(eachPart_stats)
            except OSError as e:
                print("No permissions for disk: " + partition.mountpoint)

        self.DiskStatus = {"partition_stats": partitions_stats}

    def get_ram_stats(self):
        ramStatus = psutil.virtual_memory()
        ramStatus_percent = ramStatus.percent
        ramStatus_total = ('%.2f' % (ramStatus.total / 1073741824)) + " Gb"
        ramStatus_available = (
            '%.2f' % (ramStatus.available / 1073741824)) + " Gb"
        ramStatus_used = ('%.2f' % (ramStatus.used / 1073741824)) + " Gb"
        if platform.system() != 'Windows':
            ramStatus_cached = ('%.2f' %
                                (ramStatus.cached / 1073741824)) + " Gb"
        else:
            ramStatus_cached = None

        self.RamStatus = {
            "total": ramStatus_total,
            "percent": ramStatus_percent,
            "available": ramStatus_available,
            "cached": ramStatus_cached,
            "used": ramStatus_used
        }

    def get_time_dct(self):
        current_time = time.localtime()
        time_dct = {
            "year": current_time.tm_year,
            "month": current_time.tm_mon,
            "day": current_time.tm_mday,
            "time": str(current_time.tm_hour) + ':' + str(current_time.tm_min) + ':' + str(current_time.tm_sec)
        }
        self.Time = time_dct

    def get_connections(self):
        ports = []
        connList = []
        ports = list(set(([conn.raddr[1] for conn in psutil.net_connections(
        ) if conn.status == 'ESTABLISHED'])))
        for port in ports:
            prtSm = sum(1 for conn in psutil.net_connections()
                        if conn.status == 'ESTABLISHED' and conn.raddr[1] == port)
            connList.append({'port': port, 'connections': prtSm})
        self.PortsStatus = connList