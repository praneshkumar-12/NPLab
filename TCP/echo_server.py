from twisted.internet import reactor, protocol

class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        print("Data received")
        print(f"Message from client: {data.decode()}")
        ack = f"Server received - {data.decode()}"
        self.transport.write(ack.encode())
    
class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return EchoServer()

reactor.listenTCP(8000, EchoFactory())
reactor.run()