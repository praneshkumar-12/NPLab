from twisted.internet import reactor, protocol

class StarProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
    
    def connectionMade(self):
        print("New client connected:", self.transport.getPeer())
        self.factory.clients.append(self)
    
    def connectionLost(self, reason):
        print("Client disconnected")
        self.factory.clients.remove(self)
    
    def dataReceived(self, data):
        message = data.decode().strip()

        if not self.name:
            self.name = message
            print(self.name, "has connected to the server")
        else:
            if message.startswith("@"):
                recepient, private_message = message[1:].split(":", 1)
                self.sendThroughServer(recepient, private_message)
            else:
                self.transport.write(message.encode())
    
    def sendThroughServer(self, recepient, message):
        self.transport.write(message.encode())   
        self.transport.write("Sending message...".encode())
        self.sendPrivateMessage(recepient, message)
        
    def sendPrivateMessage(self, recepient, message):
        for client in self.factory.clients:
            if client.name == recepient:
                client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                break
        else:
            self.transport.write(f"Error: User {recepient} not found\n".encode())

class StarFactory(protocol.Factory):
    def __init__(self):
        self.clients = []
    
    def buildProtocol(self, addr):
        return StarProtocol(self)

reactor.listenTCP(8080, StarFactory())
print("Server started listening on port 8080")
print("Enter client name to register. Enter @ followed by the recepient name before the starting of a new message to send a private message")
reactor.run()


# use 3 different terminals to connect to server
# telnet <ip> <port>
# telnet 127.0.0.1 8080