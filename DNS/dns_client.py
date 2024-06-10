from twisted.internet import reactor, protocol


class dns_client(protocol.Protocol):
    def connectionMade(self):
        print("connected to server")
        a = input("enter domain name:")
        self.transport.write(a.encode())

    def dataReceived(self, data):
        d = data.decode()
        if d is not None:
            print(data)
        else:
            print("invalid domain name")


class dns_client_factory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return dns_client()

    def clientConnectionFailed(self, connector, reason):
        print("connection failed")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("connection lost")
        reactor.stop()


reactor.connectTCP("localhost", 8000, dns_client_factory())
reactor.run()
