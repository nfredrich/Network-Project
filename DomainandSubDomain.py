from tld import get_fld
import os
import whois
import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

def findSubdomains():   # function that returns a list of subdomains associated with a domain
    print("""Welcome to the automated program that finds a list of subdomains for a requested domain. 
    This program requires a text document with a list of typical subdomains to search. """)
    domain = input("Enter domain to scan for subdomains without protocol (e.g without 'http://' or 'https://'):  ")
    if 'www.' in domain:
        domain = domain.replace('www.', '')
    wordlist = input("File that contains all subdomains to scan, line by line. Default is subdomains.txt: ")   # for more files go to https://github.com/rbsec/dnscan
    if wordlist == "":
        wordlist = 'subdomains.txt'
    subdomains = open(wordlist).read().splitlines()
    print("\nStarting scan...")
    for subdomain in subdomains:
        url = f"http://{subdomain}.{domain}"
        try:
            requests.get(url, timeout=6.0)
            print("[+] Discovered subdomain:", url)
        except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
            continue

    print("Search complete.\n")
    return


def isregistered(domain):  # checks if a domain is registered or not
    try:
        w = whois.query(domain)
    except:
        return False
    else:
        return bool(w)
def get_domain_name(url):  # gets the top-level domain name
    domain_name = get_fld(url)
    return domain_name

def get_ip_address(url):  # returns the ip address of a url
    command = "host " + url
    process = os.popen(command)
    results = str(process.read())
    marker = results.find( 'has address' ) + 12
    return results[marker:].splitlines()[0]


def get_domain_info():   # returns basic information about a domain

    print("This program displays basic url information including: Top Level Domain, IP adddress, and more. ")
    url = input("What url would you like to receive data about? ")
    if 'http' in url:
        strippedURL = get_domain_name(url)
    else:
        strippedURL = url

    print("\n" + strippedURL, "is registered" if isregistered(strippedURL) else "is not registered")
    if isregistered(strippedURL):
        print("\nDomain information for: " + url)
        print("     IP Address: " + get_ip_address(strippedURL))
        whoisINFO = whois.query(strippedURL)
        print("     Name (Top Level Domain): " + whoisINFO.name)
        print("     Domain Registrar: " + whoisINFO.registrar)
        print("     Domain Server: ")
        for server in whoisINFO.name_servers:
            print("          [+] {}".format(server))
        print("     Creation Date: " + str(whoisINFO.creation_date))
        print("     Expiration Date: " + str(whoisINFO.expiration_date))
    return




