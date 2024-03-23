import sys
import socket
from datetime import datetime
from dbfunctions import writeToDB
from datetime import datetime

def tstamp(): 
    dt = datetime.now()
    ts = dt.strftime("%H:%M:%S")
    return ts

def onionHandler(url):
    if url.endswith(".onion"):
        print("\n" + tstamp() + "Onion detected\n")
        writeToDB(url, "onions", "url")
        return url
    
def createRequestHeader():
    header = {"Accept" : "text/html",
              "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
              "Accept-Encoding" : "gzip, deflate, br",
              "Referer" : "127.0.0.1"}
    return header

def printError(error):
    print("\n" + tstamp() + " " + str(error))
    
