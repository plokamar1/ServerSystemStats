import psutil, json, string, time
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


CPUStats()