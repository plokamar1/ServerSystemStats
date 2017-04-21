import psutil, json

class connPorts:
    def __init__(self, name):
        self.port_name = name
        self.connections = 1

    def addConnection(self):
        self.connections += 1

def get_dict(connObjects):
    return connObjects.__dict__



def getConnections():
    retStr = ""
    i = 0
    ports = []
    connObjects = []
    for connection in psutil.net_connections():
        if connection.status == 'ESTABLISHED' :
            if connection.raddr[1] not in ports:
                ports.append(connection.raddr[1])
                connObjects.append(connPorts(connection.raddr[1]))
    
    for obj in connObjects:
        for connection in psutil.net_connections():
            if connection.status == 'ESTABLISHED' and connection.raddr[1] == obj.port_name:
                obj.addConnection()

    connsJSON = json.dumps(connObjects,default=get_dict,indent=4,sort_keys=False)
    return connsJSON

print(getConnections())
