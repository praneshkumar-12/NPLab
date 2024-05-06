from twisted.internet import reactor, protocol

class EchoServer(protocol.Protocol):
    def __init__(self, users):
        self.users = users
        self.name = None
    
    def dataReceived(self, data):
        msg = data.decode().strip()
        if self.name is None:
            self.name = msg
            self.users[msg] = self
            print(f"User {self.name} joined!")
        else:
            print(f"User {self.name} has sent: {msg}")
            broadcast_message = f"{self.name} : {msg}"
            for user in self.users.values():
                user.transport.write(broadcast_message.encode())

class EchoFactory(protocol.Factory):
    def __init__(self):
        self.users = {}
    
    def buildProtocol(self, addr):
        return EchoServer(self.users)

reactor.listenTCP(1234, EchoFactory())
reactor.run()
