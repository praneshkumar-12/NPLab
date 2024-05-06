from twisted.internet import reactor, protocol

class FileTransferServer(protocol.Protocol):
    def connectionMade(self):
        print("Connected to client.")
    
    def dataReceived(self, data):
        with open('received_file.txt', 'w+') as f:
            f.write(data.decode())

        response = "File has been transferred and saved as 'received_file.txt'"
        self.transport.write(response.encode())

class FileTransferServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return FileTransferServer()

reactor.listenTCP(8600, FileTransferServerFactory())
reactor.run()