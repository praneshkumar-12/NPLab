from twisted.internet import reactor, protocol

class EchoServer(protocol.DatagramProtocol):
    def datagramReceived(self, data, addr):
        if data.decode() == "EOF":
            print("File received!")
            print("Stopping...")
            self.transport.stopListening()
        else:
            with open('received_txt.txt', 'a+') as f:
                f.write(data.decode())
        


reactor.listenUDP(8088, EchoServer())
reactor.run()