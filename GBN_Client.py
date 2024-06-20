from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import time

class Receiver(DatagramProtocol):
    status = False
    expected_packet = 0

    def datagramReceived(self, datagram, addr) -> None:
        packet_num = int(datagram.decode()[-1])

        if packet_num == 2 and not self.status:
            self.status = True
            print('break')
            time.sleep(7)
            return

        if packet_num == self.expected_packet:
            print("Received packet", packet_num)
            ack = str(packet_num)
            self.transport.write(ack.encode(), addr)
            self.expected_packet += 1
        else:
            print("Discarded packet", packet_num)


if __name__ == "__main__":
    reactor.listenUDP(9000, Receiver())
    reactor.run()
