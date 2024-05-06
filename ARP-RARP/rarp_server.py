from twisted.internet import reactor, protocol

class RARPServer(protocol.Protocol):
    def __init__(self, table):
        self.table = table
    
    def connectionMade(self):
        print("Client connected!")
    
    def dataReceived(self, data):
        data = data.decode()
        ip = self.table.get(data)
        if ip:
            self.transport.write(ip.encode())
        else:
            self.transport.write("None".encode())

class RARPFactory(protocol.Factory):
    def __init__(self, table):
        self.table = table

    def buildProtocol(self, addr):
        return RARPServer(self.table)
    
table = {
    "00:11:22:33:44:55": "192.168.1.1"
}

reactor.listenTCP(8099, RARPFactory(table))
reactor.run()