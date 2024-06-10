from twisted.internet import protocol, reactor


class dns_server(protocol.Protocol):
    def connectionMade(self):
        print("Client connected")

    def dataReceived(self, data):
        global dns_table
        a = data.decode()
        ip = dns_table.get(a)  # Retrieve the IP address from the dns_table dictionary
        if ip is not None:
            response = f"IP for {a} is {ip}"
        else:
            response = f"No IP found for {a}"
        self.transport.write(response.encode())


class dns_factory(protocol.Factory):
    def buildProtocol(self, addr):
        return dns_server()


dns_table = {}
dns_table["www.google.com"] = "192.0.0.1"
dns_table["www.youtube.com"] = "192.0.0.2"

reactor.listenTCP(8000, dns_factory())
reactor.run()
