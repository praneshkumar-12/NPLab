from twisted.internet import reactor, protocol

class EchoClient(protocol.DatagramProtocol):
    def startProtocol(self):
        self.transport.connect('127.0.0.1', 8088)
        self.sendDatagram()
    
    def sendDatagram(self):
        data = input("Enter the data to send to server:")
        self.transport.write(data.encode())
        self.transport.stopListening()
        print("Stopped listening!")


reactor.listenUDP(0, EchoClient())
reactor.run()
