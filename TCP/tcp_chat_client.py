from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def __init__(self):
        self.name = input("Enter your name:")
    
    def connectionMade(self):
        self.transport.write(self.name.encode())
        reactor.callInThread(self.send_data)
    
    def dataReceived(self, data):
        print(data.decode())
    
    def send_data(self):
        while True:
            msg = input()
            self.transport.write(msg.encode())

class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()
    
reactor.connectTCP("localhost", 1234, EchoFactory())
reactor.run()
