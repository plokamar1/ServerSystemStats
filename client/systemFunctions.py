import psutil, json, string, time
import os

def CPUStats():
    loadAverage = os.getloadavg()

    percentPerCpu = psutil.cpu_percent(interval=1, percpu=True)
    
    nmbCores = len(percentPerCpu)
    ######################Making the json object
    #current usage first
    retStr = '{"CPUStats": {"CurrentUsage" : {'
    for i in range(1,nmbCores+1):
        retStr += '"Core_'+str(i)+'" : '+ str( percentPerCpu[i-1]/nmbCores )
        if(i < nmbCores):
            retStr += ','
    retStr += '}'
    retStr += ','
    #load average
    retStr +='"loadAverage": {'
    retStr +='"oneMinute":'+str(loadAverage[0])+','
    retStr +='"fiveMinutes":'+str(loadAverage[1])+','
    retStr +='"fifteenMinutes":'+str(loadAverage[2])+','
    retStr += '}'

    retStr +=' }}'

    print(json.dumps(json.loads(retStr ),indent=4, separators=(',', ': ')))
    return retStr

def DISKStats():
    partitions_stats = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            diskUsage = psutil.disk_usage(partition.mountpoint)
            diskUsage_gb = ('%.2f' % (diskUsage.used/1073741824)) + " Gb"
            diskIO = psutil.disk_io_counters()

            eachPart_stats ={ "Name": partition.mountpoint, "usagePercent":diskUsage.percent, "usageGB":diskUsage_gb, "read_count": diskIO.read_count , "write_count":diskIO.write_count }
            partitions_stats.append(eachPart_stats)
        except OSError as e:
            print("No permissions for disk: "+partition.mountpoint+"\n") 

    retStr = "\"PartitionStats\": [\n"
    for partition in partitions_stats:
        retStr += json.dumps({"partitionName":partition['Name'] ,"usageInGb":partition['usageGB'],"usagePercent": partition['usagePercent'],"diskRead":partition['read_count'],"diskWrite":partition['write_count']},indent=4, separators=(',', ': '))
        
    print( retStr)

DISKStats()