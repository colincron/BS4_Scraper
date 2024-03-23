import requests
from bs4 import BeautifulSoup
from functions import onionHandler, tstamp 
from classes import Domain
import socket

def mainCrawler():
    response = ""
    startUrl = input(tstamp() + " Start URL: ")
    #time.sleep(10)
    numberOfCrawls = input(tstamp() + " How many crawls do you want to do? ")
    #time.sleep(10)
    #databaseCreate = input("Do you need to create a database?")
    i = 0
    urlList = [startUrl,]

    while len(urlList) > i and int(numberOfCrawls) >= i: 
        url = urlList[i]
        print("\n" + tstamp() + " Length of urlList: " + str(len(urlList)))
        print(tstamp() + " Number of sites crawled:" + str(i) + "\n")
        
        while url.endswith("onion") or url.endswith("onion/"):
            onionHandler(url)
            url = urlList[ i + 1 ]
            i = i + 1
        
        print(tstamp() + " Now scanning: " + url)
        
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            print(tstamp() + " Connection refused")
        except socket.gaierror:
            print(tstamp() + " Connection refused")
        except requests.exceptions.TooManyRedirects:
            print(tstamp() + " Too many redirects, dude!")
        
            
        if response:
            htmlData = response.content
            parsedData = BeautifulSoup(htmlData, "lxml") #lxml is fast and lenient
            anchors = parsedData.find_all(lambda tag: tag.name == 'a' and tag.get('href'))

            for a in anchors:
                references = [a["href"]]
                for r in references:
                    if r.startswith("http") and r not in urlList:
                        urlList.append(r)
                        if r.endswith(".com/" or ".net/" or ".edu/" or ".org/" or ".io/" or ".gov/"):
                            r = Domain(r)
                            r.addServerInfo()
                            r.writeToDatabase("domains")
                            print("\n" + tstamp() + " Domain " + r.name + " written to DB\n")
        i = i + 1
        
    else:
        print(tstamp() + " All done!")


mainCrawler()