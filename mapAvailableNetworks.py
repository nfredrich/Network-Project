from scapy.all import ARP, Ether, srp
import optparse

def discoveringNetworks(targetIP):    # discovers devices connected on the same network

    target_ip = targetIP + "/24"

    arp = ARP(pdst=target_ip)
    ether = Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = ether/arp
    result = srp(packet, timeout=3)[0]
    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    print("Available devices in the network: ")
    print("IP" + " "*18 + "MAC")
    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))
    print("\nScan Complete!\n")
    return

def main():
    parser = optparse.OptionParser("usage %prog " + "-t <target network>")
    parser.add_option('-t', dest='targetIP', type='string', help='specify target network')

    (options, args) = parser.parse_args()
    target_ip = options.targetIP
    discoveringNetworks(target_ip)
    return

main()

