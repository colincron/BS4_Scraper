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