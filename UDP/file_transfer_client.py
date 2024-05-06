from twisted.internet import reactor, protocol

class EchoClient(protocol.DatagramProtocol):
    def startProtocol(self):
        self.transport.connect('127.0.0.1', 8088)
        self.sendDatagram()
    
    def sendDatagram(self):
        with open("send_file.txt", "r+") as f:
            for txt in f:
                self.transport.write(txt.encode())
        
        self.transport.write("EOF".encode())
        
        print("File Transferred!")
        print("Stopping...")
        self.transport.stopListening()

reactor.listenUDP(0, EchoClient())
reactor.run()
