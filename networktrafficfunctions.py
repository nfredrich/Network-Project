#!/usr/bin/python
# -*- coding: utf-8 -*-
from scapy.all import *
import urllib.request
import ipinfo

import filePathFunction
from getpass import getpass
import subprocess


def geoLocInfo(ip, access_token):  # returns detailed/specific information for a specific IP address using the ipinfo.io API
    try:
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(ip)
        city = details.city
        country = details.country_name
        return city + ", " + country
    except:
        return "Error with access token."


def retGeoStr(ip):  # returns less detailed geo information using the geolocation database for a specific IP address
    with urllib.request.urlopen("https://geolocation-db.com/jsonp/{0}".format(ip)) as url:
        data = url.read().decode()
        data = data.split(",")
        country_city = data[2].split(":")
        country_name = data[1].split(":")
        if country_city[1] == 'null' :
            return country_name[1]
        else:
            return country_city[1] + ", " + country_name[1]



def printPcap(pcap):   # analyzes the pcap file packet by packet returning the source and destination IP address and geo-location information
    print("This program uses the ipinfo.io API to locate geographical information related to the IP address. You must have an account to utilize this feature.")
    access_token = input("Enter the access token provided by ipinfo.io (If you have none, hit ENTER to continue): ")   # myaccount token: 07191148e07b93
    for pkt in pcap:
        if IP in pkt:
            try:
                 srcaddress = pkt[IP].src
                 dstaddress = pkt[IP].dst
                 print('\n[+] Src: ' + srcaddress + ' -->  Dst: ' + dstaddress)
                 if access_token == '':
                     print('[+] Src: ' + retGeoStr(srcaddress) + ' -->  Dst: ' + retGeoStr(dstaddress))
                 else:
                    print('[+] Src: ' + geoLocInfo(srcaddress, access_token) + ' -->  Dst: ' + geoLocInfo(dstaddress, access_token))
            except:
                print("nothing to report")
                pass


def printHeaderInfo():  # requests user input for a specific pcap file to analyze
    print("""Welcome to to the Print Direction script. 
        This script analyzes pcap network captures to find the source and destination IP information for individual packets.""")  # prints a welcome text to the screen
    pcap = input("Input the specific pcap file you wish to analyze: ")  # requests a specific pcap file as an input from the user and assigns the result to the variable pcap
    pcap = filePathFunction.checkFilePath(pcap)
    try:  # exception handling; checks if a valid file was entered by the user, if not it skips to the except clause
        packets = rdpcap(pcap)  # rdpcap() reads the pcap file and returns a packet list (the list is assigned to the packets variable)
        printPcap(packets)  # calls the printPcap() function with the packets variable as a parameter
    except:  # executes the below code if an error was thrown in the try clause
        print("Invalid Response: Please enter a valid pcap file.")  # prints an invalid response message to the screen
        printHeaderInfo()  # restarts the main function by calling main()

    print("\nAnalysis of " + pcap + " file complete.\n")  # prints the statement "Analysis of <pcap file> complete." to the screenv
    return

def createpcapFile(): # creates a pcap file recording a specific number of packets using tcpdump
    print("")
    pwd = getpass("Please enter sudo password: ")  # getpass prompts the user for a password without echoing and assigns the result as a stream object to the variable pwd
    fileName = input("What is the name of the file you wish to send the packet information to? ")  # asks user to input a decoy system and assigns the result to the decoy variable
    if '.pcap' not in fileName:
        fileName = fileName + '.pcap'
    interfaceValue = input("What interface would you prefer to capture packets on? (Default: eth0) ")
    if interfaceValue == '':
        interfaceValue = 'eth0'
    packetCount = input("How many packets should the file count/contain? (Default: 50) ")
    if packetCount == '':
        packetCount = '50'
    limitpackets = (input("Would you like to limit the search to only ftp and ssh packets? (Y/N) ")).lower()
    if limitpackets == 'y':
        print("The program WILL limit to ftp and ssh only.")
        portLimit = " port ftp or ssh "
    else:
        print("The program WILL NOT limit to ftp and ssh only.")
        portLimit = ""
    cmd = "echo " + pwd + " | sudo -S tcpdump -s 0 -c " + packetCount + portLimit +" -i " + interfaceValue + " -w " + fileName
    print("\nStarting the collection process...")
     # call is a function that runs the the cmd argument (a string) in the shell and waits for the command to complete at which point it returns the returncode attribute
    process = subprocess.call(cmd, shell=True)
    print("\nProcess complete!")  # prints "Process complete!" to the screen
    return





def spoofsniffing():  # the packet sniffing app that detects if a network is beeing spoofed
    print("Welcome to the packet sniffing app!")
    pwd = getpass("Please enter sudo password: ")
    ethernet = input("Which ethernet interface would you like to check? (Default: eth0) ") # asks the user to input their preferred interface and assigns the result to ethernet
    if ethernet == '': # if the user does input a value, THRESH is initialized to their input
        ethernet = 'eth0'
    threshold = input("What ttl difference threshold would you like? (Default = 5) ")  # user is asked to input a value for the threshold and the result is assigned to the variable threshold
    if threshold == '': # if the user does input a value, THRESH is initialized to their input
        threshold = 5
    length = input("For how many seconds would you like the detector to run? (Default: 10 seconds) ")
    if length == "":
        length = 10
    if int(length) <= 1:
        print("Error: Enter a number greater than 1")
        input("Hit ENTER to restart this session.")
        spoofsniffing()

    cmd = "echo " + str(pwd) + " | sudo -S python3 SpoofDetectNF.py -i " + str(ethernet) + " -t " + str(threshold) + " -c " + str(length)
    proc = subprocess.call(cmd, shell=True)  # call is a function that runs the the cmd argument (a string) in the shell and waits for the command to complete at which point it returns the returncode attribute
    print("\nProcess complete!\n")  # prints "Process complete!" to the screen
    pwd = ""
    return

def discover_available_networks(target_ip):  # returns a list of availalbe ip addresses on a specificed network; maps the network to find devices that are connected to the same network
    print("Welcome to the program that detects all available devices on a specified network.")
    pwd = getpass("Please enter sudo password: ")
    print("The target specified is currently: " + str(target_ip) + "/24")
    cmd = "echo " + str(pwd) + " | sudo -S python3 mapAvailableNetworks.py -t " + str(target_ip)
    print("\nScan in progress...")
    proc = subprocess.call(cmd, shell=True)  # call is a function that runs the the cmd argument (a string) in the shell and waits for the command to complete at which point it returns the returncode attribute
    return

