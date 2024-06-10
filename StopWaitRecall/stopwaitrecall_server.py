from twisted.internet import reactor, protocol


class StopAndWaitServer(protocol.Protocol):
    def send_ack(self):
        self.transport.write(input("Enter ack(ack/ACK): ").encode())

    def dataReceived(self, data):
        print("Message from client:", data.decode())
        ack = f'{"Server recieved - " + data.decode()}'
        self.send_ack()

    def connectionLost(self, reason):
        print("Client disconnected:")


class StopAndWaitServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return StopAndWaitServer()


reactor.listenTCP(8002, StopAndWaitServerFactory())
reactor.run()
