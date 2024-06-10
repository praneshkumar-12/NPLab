from twisted.internet import reactor, protocol


class StopAndWaitClient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server.")
        msg = input("Enter message to be send to server - ")
        self.transport.write(msg.encode())

    def dataReceived(self, data):
        ack = data.decode()
        if ack == "ACK" or ack == "ack":
            print("ACK received. Message acknowledged.")
            self.send_message()
        else:
            print("Invalid ACK received.")
            reactor.callLater(3, self.resend_message())

    def send_message(self):
        msg = input("Enter message to be send to server - ")
        self.transport.write(msg.encode())

    def resend_message(self):
        print("ACK not received. Resending message...")
        self.send_message()

    def connectionLost(self, reason):
        print("Connection lost:")


class StopAndWaitClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return StopAndWaitClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:")
        reactor.stop()


reactor.connectTCP("localhost", 8002, StopAndWaitClientFactory())
reactor.run()
