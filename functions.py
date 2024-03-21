import sys
import socket
from datetime import datetime
from dbfunctions import writeToDB

def createHeader():
    #add code to rotate through created headers
    return

def onionHandler(url):
    if url.endswith(".onion"):
        print("\nOnion detected\n")
        writeToDB(url, "onions", "url")
        return url
    
def stripURL(domain):
    domain = str(domain)
    print(domain)
    if domain.startswith("https") is True:
        domain = (domain.removeprefix("https://")).removesuffix("/")
        print("https removed")
    elif domain.startswith("http") is True:
        domain = (domain.removeprefix("http://")).removesuffix("/")
        print("http removed")
    print("This has no http/s-> "+ domain)
    return domain
    
def getIP(domain):
    target = socket.gethostbyname(domain) 
    # returns IPV4 address
    return target
    
def domainScout(domain):
    target = getIP(stripURL(domain))

    print("Scanning Target: " + target)
    print("Scanning started at:" + str(datetime.now()))
  
    try: 
        for port in range(1,1024):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(.25)     
            # returns error indicator
            result = s.connect_ex((target,port))
            print(result)
            if result ==0:
                print("Port {} is open".format(port))
            s.close()
         
    except KeyboardInterrupt:
        print("\n Exiting Program")
        sys.exit()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved")
        sys.exit()
    except socket.error:
        print("\n Server not responding")
        sys.exit()
    return 0