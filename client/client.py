import psutil
import time

def CPUPercent():
    return psutil.cpu_percent(interval=1, percpu=True)

if __name__ == "__main__":
    i = 1
    while ( i>0 ):
        print(CPUPercent() )
        time.sleep(30)