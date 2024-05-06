from twisted.internet import reactor, protocol

class EchoClient(protocol.DatagramProtocol):
    def __init__(self):
        self.name = input("Enter your name: ")
    
    def startProtocol(self):
        self.transport.connect("127.0.0.1", 1234)
        self.transport.write(f"Name: {self.name}".encode())
        reactor.callInThread(self.send_data)
    
    def datagramReceived(self, data, addr):
        print(data.decode())
    
    def send_data(self):
        while True:
            msg = input()
            self.transport.write(f"{self.name}: {msg}".encode())

reactor.listenUDP(0, EchoClient())
reactor.run()
