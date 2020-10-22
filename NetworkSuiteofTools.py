from Banner import banner
from networkinformationfunctions import *
from nmapfunctions import *
from networktrafficfunctions import *
from DomainandSubDomain import *
from cryptofunctions import *


target = ""

def localHostInfo():   # calls functions that return the local host information like MAC Address, IP address, etc.
    networkInfo()
    decisions()
    return

def ping():  # calls functions that pings a target system
    global target
    target = pingTarget(target)
    decisions()
    return

def traceroute():  # calls functions that shows the route taken by packets across an IP network
    global target
    target = traceTheRoute(target)
    decisions()
    return

def portScanner():   # calls functions that scans specified ports of a target system
    global target
    target = checkHostName(target)
    portScannerOptions(target)
    decisions()
    return


def spoofDetect():   # calls functions that will detect if spoofed packets are being sent to the host computer
    spoofsniffing()
    decisions()
    return


def nmapDecoy():  # will send spoofed packets to a target system
    global target
    print("Greetings and welcome to the nmapDecoy app!")  # prints a greeting to the screen
    target = checkHostName(target)
    decoyFunction(target)
    decisions()
    return

def printDirection():  # prints the source and destination ip addresses of packets from a pcap file
    printHeaderInfo()
    decisions()
    return

def createpcap():  # creates a pcap file that records network traffic
    print("This program generates a pcap file of the current network traffic with various options.")
    createpcapFile()
    decisions()
    return

def availableNetworks():  # calls functions that maps the network to find devices that are connected to the same network
    global target
    target = checkHostName(target)
    discover_available_networks(target)
    decisions()
    return

def clientTunnel():  # creates a tcp tunnel that you can send encrypted messages over
    print("This program will send an ecrypted message via a tcp tunnel to a target system. ")
    connectClient()
    decisions()
    return

def serverTunnel(): # creates a tcp tunnel that you can send encrypted messages over
    print("This program will receive an encrypted message via a tcp tunnel from some system.")
    connectServer()
    decisions()
    return

def domainInfo(): # calls functions that prints the domain information for a given domain
    get_domain_info()
    decisions()
    return

def subdomain():  # calls function that lists all the subdomains of a specificed domain
    findSubdomains()
    decisions()
    return


def sessionswitcher(argument): # defines the function that gets the dictionary value we need that is associated with the userinput key (regarding the main menu options and which session we are doing)
    switcher = menu()   # calls the menu() function and generates our dictionary object
    func = switcher.get(argument, "Nothing") # gets the value associated with the argument (our value) from the dictionary and assigns the result to func (if it does not exist it returns "Nothing")
    return func()  # returns the variable func but turns it into a function call (it calls the session functions for 8.1-8.6)

def decisions():  # defines the function that loops our program so the user chooses when to exit the program
    stayorgo = (input("Would you like to return to the main menu? Please enter 'y' to return to the main menu and 'n' to exit the program: ")).lower()  # requests user input regarding whether they wish to continue the program or exit and assigns the result to stayorgo
    if stayorgo == "y":  # if the variable stayorgo contains the value 'yes' execute the main() function again, otherwise skip to the elif statement
        main()
    elif stayorgo == "n": # if the variable stayorgo contains the value 'no' execute the below code, otherwise skip to the else clause
        print("Goodbye!") # prints "Goodbye!" to the screen
        exit(0) # clean exit of the program with no errors
    else: # if none of the above are true, execute the below code (catches any unintended answers like numbers or accidental typoes)
        decisions() # calls the decisions() function (recursion)

def menu():  # defines the function that creates a dictionary object containing our menu of options assigned to a number
    mymenu = {
        1: localHostInfo,
        2: ping,
        3: traceroute,
        4: portScanner,
        5: spoofDetect,
        6: nmapDecoy,
        7: printDirection,
        8: createpcap,
        9: availableNetworks,
        10: clientTunnel,
        11: serverTunnel,
        12: domainInfo,
        13: subdomain,
        14: decisions
    }
    return mymenu # returns the dictionary object assigned to the variable mymenu to the original function call
def main():
    banner()  # calls the banner function (prints the banner to the screen)
    try:  # exception handling that executes the try clause and finishes unless an error is thrown (in which case it skips to the except clause) -> catches the errors thrown by int()
        userinput = int(input("Enter the number of program you wish to run: "))  # requests user input and assigns the result (converted into an integer) to the variable userinput
    except: # executes except clause if there was an error in the try clause
        input("That is an invalid response. Hit ENTER to return to the main menu and re-enter a number between 1-14.") # requests user input again and states there was an issue with their response
        main() # calls the main() function
    if userinput > 0 and userinput < 15: # checks if the value given by the user is between 1 and 6, if not it skips to the else clause
        sessionswitcher(userinput) # calls teh sessionswitcher() function
    else: # executes below code if userinput was not between 1 and 6
        input("That is an invalid response. Hit ENTER to return to the main menu and re-enter a number between 1-14.") # requests user input again and states there was an issue with their response
        main() # calls the main() function


main()