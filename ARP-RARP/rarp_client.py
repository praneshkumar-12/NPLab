from twisted.internet import reactor, protocol

class RARPClient(protocol.Protocol):
    def connectionMade(self):
        ip = input("Enter MAC Address:")
        self.transport.write(ip.encode())
    
    def dataReceived(self, data):
        ip = data.decode()
        if ip != "None":
            print(f"IP Address: {ip}")
        else:
            print("Invalid Mac!")

class RARPFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return RARPClient()

    def clientConnectionLost(self, connector, reason):
        print('Connection lost')
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed')
        reactor.stop()

reactor.connectTCP("localhost", 8099, RARPFactory())
reactor.run()
