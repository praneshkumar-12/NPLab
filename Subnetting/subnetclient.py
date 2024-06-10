from twisted.internet import protocol, reactor


class subnetclient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server")
        ip = input("Enter ip addr:")
        subnetmask = input("Enter subnet mask addr :")
        msg = f"{ip}/{subnetmask}"
        self.transport.write(msg.encode())

    def dataReceived(self, data):
        reply = data.decode()
        check, host = reply.split(":", 1)  # format - valid:noofhosts
        if check == "valid":
            print(host)

        else:
            print("Invalid IP/Subnet mask.")


class subnetclientfactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return subnetclient()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost")
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed")
        reactor.stop()


reactor.connectTCP("localhost", 7429, subnetclientfactory())
reactor.run()
