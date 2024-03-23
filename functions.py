import sys
import socket
from datetime import datetime
from dbfunctions import writeToDB
from datetime import datetime

def tstamp(): 
    dt = datetime.now()
    ts = dt.strftime("%H:%M:%S")
    return ts

def createHeader():
    #add code to rotate through created headers
    return

def onionHandler(url):
    if url.endswith(".onion"):
        print("\n" + tstamp() + "Onion detected\n")
        writeToDB(url, "onions", "url")
        return url
    
