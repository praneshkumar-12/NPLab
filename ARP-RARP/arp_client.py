from twisted.internet import reactor, protocol

class ARPClient(protocol.Protocol):
    def connectionMade(self):
        ip = input("Enter IP Address:")
        self.transport.write(ip.encode())
    
    def dataReceived(self, data):
        mac = data.decode()
        if mac != "None":
            print(f"Mac Address: {mac}")
        else:
            print("Invalid IP!")

class ARPFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return ARPClient()

    def clientConnectionLost(self, connector, reason):
        print('Connection lost')
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed')
        reactor.stop()

reactor.connectTCP("localhost", 8099, ARPFactory())
reactor.run()
