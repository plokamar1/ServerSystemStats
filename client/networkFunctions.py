import psutil, json

class connPorts:
    def __init__(self, name):
        self.name = name
        self.connections = 1

    def addConnection(self):
        self.connections += 1

def getConnections(port):
    retStr = ""
    i = 0
    ports = []
    connObjects = []
    for connection in psutil.net_connections():
        if connection.status == 'ESTABLISHED' :
            if connection.raddr[1] not in ports:
                ports.append(connection.raddr[1])
                connObjects.append(connPorts(name = connection.raddr[1]))
    
    for obj in connObjects:
        for connection in psutil.net_connections():
            if connection.status == 'ESTABLISHED' and connection.raddr[1] == obj.name:
                obj.addConnection()

    for connObject in connObjects:
        #print( str(connObject.name)+" : "+str(connObject.connections))
        retStr += json.dumps({"PortName": connObject.name , "Connections" : connObject.connections},indent=4, separators=(',', ': '))

    print(retStr)

getConnections(3306)