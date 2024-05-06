from twisted.internet import reactor, protocol

class EchoServer(protocol.DatagramProtocol):
    def datagramReceived(self, data, addr):
        print("Message from client:", data.decode())
        self.transport.stopListening()
        print("Stopped listening!")

reactor.listenUDP(8088, EchoServer())
reactor.run()