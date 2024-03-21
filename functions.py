import sys
import socket
from datetime import datetime
from dbfunctions import writeToDB

def onionHandler(url):
    if url.endswith(".onion"):
        print("\nOnion detected\n")
        writeToDB(url, "onions", "url")
        return url
    
def domainScout(domain):
    domain = str(domain)
    print(domain)
    if domain.startswith("https") is True:
        domain = domain.removeprefix("https://")
        domain = domain.removesuffix("/")
        print("https removed")
    elif domain.startswith("http") is True:
        domain = domain.removeprefix("http://")
        domain = domain.removesuffix("/")
        print("http removed")
    print("This has no http/s-> "+ domain)
    target = socket.gethostbyname(domain) 

    print("Scanning Target: " + target)
    print("Scanning started at:" + str(datetime.now()))
  
    try: 
        for port in range(1,65535):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)     
            # returns error indicator
            result = s.connect_ex((target,port))
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