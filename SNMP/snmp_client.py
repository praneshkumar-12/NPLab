from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol


class SNMPClientProtocol(DatagramProtocol):
    def startProtocol(self):
        self.transport.connect("127.0.0.1", 161)
        self.sendRequest()

    def sendRequest(self):
        request = "SNMP request"
        self.transport.write(request.encode())

    def datagramReceived(self, data, addr):
        print(
            "Received data from {}: {}".format(addr, data)
        )  # Process the SNMP response here


def run_client():
    reactor.listenUDP(0, SNMPClientProtocol())
    reactor.run()


run_client()
