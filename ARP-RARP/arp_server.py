from twisted.internet import reactor, protocol

class ARPServer(protocol.Protocol):
    def __init__(self, table):
        self.table = table
    
    def connectionMade(self):
        print("Client connected!")
    
    def dataReceived(self, data):
        data = data.decode()
        mac = self.table.get(data)
        if mac:
            self.transport.write(mac.encode())
        else:
            self.transport.write("None".encode())

class ARPFactory(protocol.Factory):
    def __init__(self, table):
        self.table = table

    def buildProtocol(self, addr):
        return ARPServer(self.table)
    
table = {
    "192.168.1.1": "00:11:22:33:44:55"
}

reactor.listenTCP(8099, ARPFactory(table))
reactor.run()