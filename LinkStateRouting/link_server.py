from twisted.internet import protocol, reactor


class echo(protocol.Protocol):
    def connectionMade(self):
        print("client connected")

    def dataReceived(self, data):
        rec = eval(data.decode())
        souce = rec.get("source")
        edges = rec.get("graph")
        source = int(souce)
        dis = [5000 for i in range(10)]
        print(edges)
        dis[source] = 0
        n = rec.get("vertices")
        for k in range(n - 1):
            for i in edges:
                u = i[0]
                v = i[1]
                wt = i[2]
                if dis[v] > wt + dis[u]:
                    dis[v] = wt + dis[u]
        # print(dis)
        send = ""
        for i in range(source, n + 1):
            send += " " + str(dis[i])
        self.transport.write(send.encode())

    def connectionLost(self, reason):
        print("client removed")
        return


class echofactory(protocol.Factory):
    def buildProtocol(self, addr):
        return echo()


reactor.listenTCP(8012, echofactory())
reactor.run()
