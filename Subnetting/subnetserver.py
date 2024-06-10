from twisted.internet import protocol, reactor
import ipaddress


def validate_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    if parts[0] == "0":
        return False  #'0.55.197.45' is an invalid ip,as no starting 0 in ip.
    else:
        for part in parts:
            if not (int(part) >= 0 and int(part) <= 255) or part.isdecimal() is False:
                return False
    return True


def validate_subnetmask(sub_mask):
    parts = sub_mask.split(".")
    if len(parts) == 4:
        return True
    else:
        return False


def calculate_network_address(ip, subnet_mask):
    ip_address = ipaddress.IPv4Address(ip)
    subnet = ipaddress.IPv4Network(ip + "/" + subnet_mask, strict=False)
    network_address = str(subnet.network_address)
    return network_address


def calculate_broadcast_address(ip, subnet_mask):
    ip_address = ipaddress.IPv4Address(ip)
    subnet = ipaddress.IPv4Network(ip + "/" + subnet_mask, strict=False)
    broadcast_address = str(subnet.broadcast_address)
    return broadcast_address


def count_zero(binary_str):
    str = "".join(reversed(binary_str))
    n = len(str)
    count = 0
    for i in str:
        if i == "0":
            count += 1
        elif i == "1":
            break

    return count


class subnettingprotocol(protocol.Protocol):
    def connectionMade(self):
        print("Connected to client")

    def dataReceived(self, data):
        data = data.decode()
        ip, subnetmask = data.split("/")
        isvalidip = validate_ip(ip)
        isvalidsubnetmask = validate_subnetmask(subnetmask)
        if isvalidip is True and isvalidsubnetmask is True:
            print("Network address :", calculate_network_address(ip, subnetmask))
            print("Broadcast address :", calculate_broadcast_address(ip, subnetmask))

            # now calculating no of hosts.
            subnet_mask_binary = ipaddress.IPv4Network("0.0.0.0/" + subnetmask)
            noofhost = subnet_mask_binary.num_addresses - 2  # formula
            reply1 = "valid"
            reply2 = f"No of hosts for {ip}/{subnetmask} is : {noofhost}"
            reply = f"{reply1}:{reply2}"
            self.transport.write(reply.encode())
        else:
            print("Invalid IP or Subnet mask")
            return


class subnetfactory(protocol.Factory):
    def buildProtocol(self, addr):
        return subnettingprotocol()


reactor.listenTCP(7429, subnetfactory())
reactor.run()
