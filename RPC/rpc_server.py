from twisted.internet import reactor, protocol


class RPCServer(protocol.Protocol):
    def connectionMade(self):
        print("Client connected.")

    def dataReceived(self, data):
        global rec

        rec = eval(data.decode())
        a = rec.get("func")
        # Check if the function exists
        if hasattr(self, a):
            # Call the function and get the result
            result = getattr(self, a)()

            # Send the result back to the client
            self.transport.write(result.encode())
        else:
            self.transport.write("bye".encode())

    def connectionLost(self, reason):
        print("client disconnected")

    def add_numbers(self):
        a = rec.get("inpu")
        return str(a[0] + a[1])


class RPCServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return RPCServer()


reactor.listenTCP(8010, RPCServerFactory())
print("Server started on port 8000.")
reactor.run()
