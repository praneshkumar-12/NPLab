from twisted.internet import protocol, reactor

class BusProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
    
    def connectionMade(self):
        self.factory.clients.append(self)
        print("New client connected")
        
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Client disconnected")
    
    def dataReceived(self, data):
        message = data.decode().strip()
    
        if not self.name:
            self.name = message
            print(f"{self.name} connected to bus")
        else:
            if message.startswith("@"):
                recepient, private_message = message[1:].split(":", 1)
                self.sendPrivateMessage(recepient, private_message)
            else:
                print(f"{self.name}: {message}")
                self.broadcastMessage(f"{self.name}: {message}")
    
    def sendPrivateMessage(self, recepient, message):
        for client in self.factory.clients:
            if client.name == recepient:
                client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                break
        else:
            self.transport.write(f"Error: User {recepient} not found\n".encode())
    
    def broadcastMessage(self, message):
        for client in self.factory.clients:
            if client.name != self.name:
                client.transport.write(f"{message}\n".encode())


class BusFactory(protocol.Factory):
    def __init__(self):
        self.names = []
        self.clients = {}
    
    def buildProtocol(self, addr):
        return BusProtocol(self)

reactor.listenTCP(8080, BusFactory())
print("Server started. Listening on port 8080...")
print("Enter client name to register. Enter @ before the starting of a message to send message to another client.")
reactor.run()
