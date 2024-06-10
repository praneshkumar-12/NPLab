from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        global a
        print("connected to the server..")
        n = int(input("enter no of vertices:"))
        """run a loop and create a edge list depending on the input graph """
        edges = [
            [2, 5, -1],
            [1, 2, 6],
            [5, 7, 3],
            [3, 5, 1],
            [3, 2, -2],
            [6, 7, 3],
            [4, 6, -1],
            [1, 4, 5],
            [1, 3, 5],
            [4, 3, -2],
        ]

        a = input("enter source vertex:")  # give source vertex as 1 during input

        to_serv = {"source": a, "graph": edges, "vertices": n}

        self.transport.write(str(to_serv).encode())

    def dataReceived(self, data):
        print(f"shortest distance from vertex {a} is {data.decode()}")
        # print ("Server said:", data)
        self.transport.loseConnection()


class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()


reactor.connectTCP("localhost", 8012, EchoFactory())
reactor.run()
