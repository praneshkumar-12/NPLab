from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol


class SNMPProtocol(DatagramProtocol):
    def datagramReceived(self, data, addr):
        print("Received data from {}: {}".format(addr, data))
        # Process the SNMP request here and prepare the response
        response = "SNMP response"
        self.transport.write(response.encode(), addr)


def run_server():
    reactor.listenUDP(161, SNMPProtocol())
    reactor.run()


run_server()
