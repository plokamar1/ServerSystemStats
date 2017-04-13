import psutil, json, string, time
from bitmath import *
import os

def CPUStats():
    loadAverage = os.getloadavg()

    percentPerCpu = psutil.cpu_percent(interval=1, percpu=True)
    
    nmbCores = len(percentPerCpu)

    retStr = "\"CPUStats\": [\n\t\"CurrentUsage\"{"
    for i in range(1,nmbCores+1):
        retStr += "\n\t\t\"Core_"+str(i)+"\" : \""+ str( percentPerCpu[i-1]/nmbCores ) +""
        if(i < nmbCores):
            retStr += ','
    retStr += "\n\t},\n"
    avgTimes = len(loadAverage)
    retStr +="\t\"loadAverage\": {\n"
    retStr +="\t\t\"oneMinute\":\""+str(loadAverage[0])+"\",\n"
    retStr +="\t\t\"fiveMinutes\":\""+str(loadAverage[1])+"\",\n"
    retStr +="\t\t\"fifteenMinutes\":\""+str(loadAverage[2])+"\"\n"
    retStr +="\t}\n]"
    print(retStr)

def DISKStats():
    partitions_stats = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            diskUsage = psutil.disk_usage(partition[1])
            diskUsage_gb = ('%.2f' % (diskUsage[1]/1073741824)) + " Gb"

            diskIO = psutil.disk_io_counters()
            print(diskIO)

            eachPart_stats ={ "Name": partition[1], "usagePercent":diskUsage[3], "usageGB":diskUsage_gb, "read_count":diskIO[0], "write_count":diskIO[1] }
            partitions_stats.append(eachPart_stats)
        except OSError as e:
            print("No permissions for disk: "+partition[1]+"\n") 

    retStr = "\"PartitionStats\": [\n"
    for partition in partitions_stats:
        retStr += json.dumps({"partitionName":partition['Name'] ,"usageInGb":partition['usageGB'],"usagePercent": partition['usagePercent'],"diskRead":partition['read_count'],"diskWrite":partition['write_count']},indent=4, separators=(',', ': '))
        print(retStr)

DISKStats()