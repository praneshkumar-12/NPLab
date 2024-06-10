from twisted.internet import reactor, protocol


class RPCClient(protocol.Protocol):
    def connectionMade(self):
        # Call the remote function
        a = input("enter function name:")
        self.callRemoteFunction(a)

    def callRemoteFunction(self, function_name):
        # Send the name of the function to the server
        a = int(input("enter a no:"))
        b = int(input("enter no 2:"))
        dic = {"func": function_name, "inpu": [a, b]}
        self.transport.write(str(dic).encode())

    def dataReceived(self, data):
        # Receive the result from the server
        result = data.decode()
        print("Result:", result)


class RPCClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return RPCClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()


reactor.connectTCP("localhost", 8010, RPCClientFactory())
reactor.run()
