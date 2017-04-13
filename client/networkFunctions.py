import psutil
i=0
for connection in psutil.net_connections():
    if connection.status == 'ESTABLISHED' and connection.laddr[1]==80 :
        i+=1

print(i)