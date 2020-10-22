import subprocess
import platform

hostname = ""

def getHostName(): # defines the function that gets the hostname from the user
    global hostname # declares hostname as a global variable and allows you to change it within the function
    hostname = input("\nEnter the target hostname: ") # prints a user request to the screen for a target hostname and assigns the result to the variable hostname
    print()
    return hostname  # returns hostname to the original function call

def checkHostName(targetName):   # checks if there is target hostname
    if targetName == '':
        targetName = getHostName()
    print("\nThe target hostname is currently " + str(targetName))
    validity = input("Is this the correct hostname/target IP? (Y/N) ").lower()
    while validity != 'y':
        print("\nChanging the hostname....")
        print("The target hostname is currently " + str(targetName))
        targetName = getHostName()
        print("The target hostname is NOW " + str(targetName))
        validity = input("Is this correct? (Y/N) ")
        print()
    return targetName


def networkInfo():  # prints the network informatino for the host system to the screen (ip address, MAC address, etc.)
    systemplatform = platform.system()
    if systemplatform == 'Linux':
        try:
            handle = Popen('ifconfig', stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)  # Popen executes a child program in a new process (on Windows it calls the CreateProcess() function)
            for line in handle.stdout.readlines():  # iterator function that iterates through each line of the process output stored in the handle variable
                line = line.decode('utf-8')  # decodes the byte information using the utf-8 processes and assigns the result to line
                print(line.rstrip())
        except:
            print("\nList of Network Interfaces:")
            subprocess.call('ip address', shell=True)
            print("\nSystem's Kernel Routing Table:")
            subprocess.call('ip route', shell=True)
            print()
    elif systemplatform == 'Windows':
        print()
        subprocess.call('ipconfig', shell=True)
        print()
    else:
        print("The network information could not be determined.")
    return

def pingTarget(targetName):  # pings a target host
    global hostname
    hostname = checkHostName(targetName)
    systemplatform = platform.system()
    if systemplatform == 'Linux':
        cmd = "ping -c 4 " + hostname
    elif systemplatform == 'Windows':
        cmd = "ping " + hostname
    else:
        print("Could not perform traceroute on current system.")
        return hostname
    returned_value = subprocess.call(cmd, shell=True)
    return hostname

def traceTheRoute(targetName):  # shows the route taken by packets across an IP network
    global hostname
    hostname = checkHostName(targetName)
    systemplatform = platform.system()
    if systemplatform == 'Linux':
        cmd = "traceroute " + hostname
    elif systemplatform == 'Windows':
        cmd = "tracert " + hostname
    else:
        print("Could not perform traceroute on current system.")
        return hostname
    returned_value = subprocess.call(cmd, shell=True)
    print("\nProcess Completed!\n")
    return hostname
