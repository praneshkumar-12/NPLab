from twisted.internet import reactor, protocol

class EchoServer(protocol.DatagramProtocol):
    def __init__(self):
        self.users = {}
    
    def datagramReceived(self, data, addr):
        msg = data.decode().strip()
        if msg.startswith("Name: "):
            self.users[msg.split(": ")[1]] = addr
            print(msg.split(": ")[1], "joined!")
        else:
            print(msg)
            for user_addr in self.users.values():
                if user_addr != addr:
                    self.transport.write(msg.encode(), user_addr)

reactor.listenUDP(1234, EchoServer())
reactor.run()
