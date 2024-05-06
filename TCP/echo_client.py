from twisted.internet import protocol, reactor

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        msg = input("Enter the message to transmit: ")
        self.transport.write(msg.encode())
    
    def dataReceived(self, data):
        print(data.decode())
        self.transport.loseConnection()

class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()
    
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

reactor.connectTCP("localhost", 8000, ClientFactory())
reactor.run()