def banner():  # defines the banner function that assigns ASCII art to the variable splashscreen and prints the result to the screen
    splashscreen = """
   _______________                         _______________ 
  |  ___________  |    __________         |  ___________  |
  | |           | |    |\      /|         | |           | |
  | |   0   0   | |    | \    / |         | |   0   0   | |
  | |     -     | |    |  \  /  |         | |     -     | |
  | |   \___/   | |    |   \/   |         | |   \___/   | |
  | |___     ___| |    |        |         | |___________| |
  |_____|\_/|_____|    |________|         |_______________|
    _|__|/ \|_|_.............*.............._|________|_
   / ********** \                          / **********  \     Nicole Fredrich
 /  ************  \                      /  ************  \             CYBR505 - Final Project
--------------------                    --------------------                   A Suite of Network Analysis Tools
"""
    print(splashscreen)
    print("Welcome to CYBR505 Final Project. This program provides the user a suite of tools that will aid them in Network Analysis")  # prints the string in the parenthesis to the screen
    print("""This program gives you the following options: 
    1: Retrieve the Local Host Network Information (IP address, MAC address, etc.)  
    2: Ping a target system.
    3: Traceroute
    4: Port Scanner
    5: Detect potential spoofed packets (A live scan).  
    6: Create an instance of an nmap decoy scan. 
    7: Analyze PCAP files recording network traffic packets to determine their source and destination IP addresses. 
    8: Generate a pcap file of live network traffic using tcpdump. 
    9: Discover the available networks on a target ip address.
    10: Send an encrypted message over a TCP tunnel (Client).
    11: Receive an encrypted message over a TCP tunnel and decrypt it (Server)
    12: Retrieve information regarding a specific domain. 
    13: Create a list of subdomains for a requested domain. 
    14: Exit Program
    """)