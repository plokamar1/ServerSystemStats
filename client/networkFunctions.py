import psutil
import json


class ConnPorts:
    def __init__(self, name):
        self.port_name = name
        self.connections = 1

    def add_connection(self):
        self.connections += 1


def get_dict(connObjects):
    return connObjects.__dict__


def get_connections():
    retStr = ""
    i = 0
    ports = []
    connObjects = []
    for connection in psutil.net_connections():
        if connection.status == 'ESTABLISHED':
            if connection.raddr[1] not in ports:
                ports.append(connection.raddr[1])
                connObjects.append(ConnPorts(connection.raddr[1]))

    for obj in connObjects:
        for connection in psutil.net_connections():
            if connection.status == 'ESTABLISHED' and connection.raddr[1] == obj.port_name:
                obj.add_connection()

    connsJSON = json.dumps(connObjects, default=get_dict,
                           indent=4, sort_keys=False)
    return connsJSON


print(get_connections())
