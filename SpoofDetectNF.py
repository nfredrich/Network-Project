#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
from scapy.all import *   # imports Python functions that enable users to send, sniff, dissect, and forge network packets
from IPy import IP as IPTEST   # imports from IPy the IP class and renames it IPTEST (IP can detect about a dozen different ways of expressing IP addresses and networks, parse them and distinguish between IPv4 and IPv6 addresses)


ttlValues = {}   #intitializes the variable ttlValues to the empty dictionary
THRESH = 5  # initializes the variable THRESH to an initial value of 5


def checkTTL(ipsrc, ttl):  # start of the function that checks the TTL
    global ttlValues
    if IPTEST(ipsrc).iptype() == 'PRIVATE':  # checks if the IP address is a private IP address (10.0. 0.0 – 10.255. 255.255 , 172.16. 0.0 – 172.31. 255.255 , 192.168. 0.0 – 192.168. 255.255)
        return # exits the checkTTL function and returns by passing None to the original function call

    if ipsrc not in ttlValues:  # checks if the source IP address is in the ttlValues (a dictionary object); if it is not we execute the if clause, otherwise skip to the next if clause
        pkt = sr1(IP(dst=ipsrc) / ICMP(), \
          retry=0, timeout=1, verbose=0)   # sr1() sends 1 packet to the ipsrc and receives an answer; returns one packet that answered the packet sent and assigns that packet to the variable pkt
        ttlValues[ipsrc] = pkt.ttl  # adds the source address of the pkt to the ttlValues dictionary as the key and the ttl value from the packet as the value

    if abs(int(ttl) - int(ttlValues[ipsrc])) > THRESH:  # checks if the absolute value of the difference of the ttl and the ip address ttl stored in the dictionary is greater than the THRESH=5
        print('\n[!] Detected Possible Spoofed Packet From: '\
          + ipsrc)  # prints the statement "Detected Possible Spoofed Packet From: <source IP address>" to the screen
        print( '[!] TTL: ' + ttl + ', Actual TTL: ' \
            + str(ttlValues[ipsrc])) # prints the spoofed ttl value and the actual ttl value associated with the source IP to the screen


def testTTL(pkt):  # start of function that tests each packet detected by the sniffing function
    try:  # exception handling; if an error is thrown at any point then the except clause is executed
        if pkt.haslayer(IP): # checks if there is an IP layer in the packet, if not it skips
            ipsrc = pkt.getlayer(IP).src # retrieves the source IP address from the packet and assigns the result to the variable ipsrc
            ttl = str(pkt.ttl) # converts the ttl requested from the pkt to a string and assigns the result to the variable ttl
            checkTTL(ipsrc, ttl) # calls the checkTTL() function using the ipsrc and ttl as parameters
    except:
        pass # null operator, passes out of the function


def detectionofspoof(): # start of the main function
    global THRESH
    parser = optparse.OptionParser("usage %prog " + \
                                   "-i <interface> -t <thresh> -c <timeout>")
    parser.add_option('-i', dest='iface', type='string', \
                      help='specify network interface')
    parser.add_option('-t', dest='thresh', type='int',
                      help='specify threshold count ')
    parser.add_option('-c', dest='length', type='int', help='specify length of scan in seconds')

    (options, args) = parser.parse_args()
    conf.iface = options.iface
    THRESH = options.thresh
    length = options.length
    print("Detection in progress...")  # prints "Detection in progress..." to the screen
    sniff(prn=testTTL, store=0, timeout=int(length))  # sniff packets off the wire and passes the function testTTL as an argument so each packet is sniffed using testTTL as the analyzing function and the function will not store any data (store=0)
    return

detectionofspoof()
