from twisted.internet import reactor, protocol

class FileTransferClient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server.")

        with open('send_file.txt', 'r+') as f:
            for txt in f:
                self.transport.write(txt.encode())
    
    def dataReceived(self, data):
        print(data.decode())

class FileTransferClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return FileTransferClient()

    def clientConnectionFailed(self, connector, reason):
        print ("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print ("Connection lost.")
        reactor.stop()

reactor.connectTCP("localhost", 8600, FileTransferClientFactory())
reactor.run()