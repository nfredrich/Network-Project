import nmap
import filePathFunction
from getpass import getpass   # imports the function getpass from the module getpass
from subprocess import * # imports all functions from the module subprocess (which spawns new processes) directly into the namespace


def nmapScan(tgtHost, tgtPort):  # function that retrieves the state of the port on the target system
    nmScan = nmap.PortScanner() # assigns the variable nmScan to the output of the function PortScanner() from the nmap module (the function creates a PortScanner object)
    nmScan.scan(tgtHost, tgtPort)  # scans the tgtHost (IP address) and the specified port in tgtPort
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state'] #gets state of port <tgtPort>/tcp on host <tgtHost>(open/closed)
    print("[*] " + tgtHost + " tcp/" + tgtPort + " " + state)  # prints the statement "[*] <tgtHost> tcp/ <tgtPort> <state>" to the screen

def portScannerOptions(targetSystem):  #should the file with a list of ports be located in the same file directory or should I use the earthquake code so it is outside the directory?????
    tgtHost = targetSystem
    print("""\nThere are 2 options available for specifying the target port[s]: 
    (1) Specify the target port[s] in a comma separated list 
    (2) Specify a list of ports in a text file
    """)
    portInputOption = input("Enter a '1' or a '2' to specify which option you wish to use: ")
    try:
        if portInputOption == '1':
            tgtPorts = str(input("Specify the comma separated list of target port[s]: ")).replace(' ', '')
            tgtPorts = tgtPorts.split(',')
            for tgtPort in tgtPorts:
                nmapScan(tgtHost, tgtPort)
            print("Scan Complete!\n")
        elif portInputOption == '2':
            tgtPortsFile = input("Enter the name of the txt file containing the list of target ports: ")
            tgtPortsFile = filePathFunction.checkFilePath(tgtPortsFile)
            portFile = open(tgtPortsFile)
            for line in portFile.readlines():
                port = line.strip('\n')
                nmapScan(tgtHost, port)
            print("Scan Complete!\n")
        else:
            input("Invalid Option: Please hit ENTER to continue and return to the portscanner option menu.")
            portScannerOptions(tgtHost)
    except:
        input("Error occurred with Port List. Review your entry and hit Enter to continue.")
        portScannerOptions(tgtHost)
    return


def decoyFunction(target):  # defines the start of the nmapDecoy function which automates the nmap functionality that sends packets to a target system using a decoy IP
    pwd = getpass("Please enter sudo password: ")  # getpass prompts the user for a password without echoing and assigns the result as a stream object to the variable pwd
    decoy = input("What is the decoy address you wish to use? (Default: 8.8.8.8) ") # asks user to input a decoy system and assigns the result to the decoy variable
    if decoy == '':
        decoy = '8.8.8.8'
    ttl = input("Enter your preferred ttl (Default: 13): ") # asks user to input a ttl number and assigns the result to the ttl variable
    if ttl == '':
        ttl = '13'
    try:  # exception  handling; executes the try clause which is the command line process for a linux and if an error is raised the except clause is executed (Windows process)
        cmd = "echo " + pwd + " | sudo -S nmap " + target + " -D " + decoy + " -ttl " + ttl  # assigns the command line prompt string that initiates nmap to the variable cmd
        print("\nStarting the decoy attempt:")  # prints "Starting the decoy attempt:" to the screen
        proc = call(cmd, shell=True)  # call is a function that runs the the cmd argument (a string) in the shell and waits for the command to complete at which point it returns the returncode attribute
        print("\nProcess complete!")  # prints "Process complete!" to the screen

    except:  # executes the below code if the try clause throws an exception
        c = "nmap " + target + " -D " + decoy + " --ttl " + ttl  # assigns the command line prompt string that initiates nmap to the variable c
        handle = Popen(c, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)  # Popen executes a child program in a new process (on Windows it calls the CreateProcess() function)
        for line in handle.stdout.readlines():  # iterator function that iterates through each line of the process output stored in the handle variable
            line = line.decode('utf-8') # decodes the byte information using the utf-8 processes and assigns the result to line
            print(line.rstrip()) # strips away any whitespace/trailing characters (in this case \r and \n) and prints the remaining line to the screen
    pwd = ''  # assigns the empty string to pwd (replaces the stored password)
    return