import requests
from bs4 import BeautifulSoup
from functions import onionHandler, tstamp, createRequestHeader, printError
from classes import Domain
import socket
import sys

def mainCrawler():
    response = ""
    startUrl = input(tstamp() + " Start URL: ")
    #numberOfCrawls = input(tstamp() + " How many crawls do you want to do? ")
    numberOfCrawls = 5000
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
        
        header = createRequestHeader()
        
        try:
            response = requests.get(url, headers=header)
        except requests.exceptions.ConnectionError as error:
            printError(error)
        except socket.gaierror as error:
            printError(error)
        except requests.exceptions.TooManyRedirects as error:
            printError(error)
        except requests.exceptions.InvalidURL as error:
            printError(error)
        except requests.exceptions.InvalidSchema as error:
            printError(error)
        
            
        if response:
            htmlData = response.content
            parsedData = BeautifulSoup(htmlData, "lxml") #lxml is fast and lenient
            anchors = parsedData.find_all(lambda tag: tag.name == 'a' and tag.get('href'))

            for a in anchors:
                references = [a["href"]]
                for r in references:
                    if r.startswith("http") and r not in urlList:
                        urlList.append(r)
                        if r.endswith(".com/" or ".net/" or ".edu/" or ".org/" or ".io/" or ".gov/" or ".co/" or ".uk/" or ".us/"
                                       or ".ai/" or ".io/" or ".info/" or ".xyz/" or ".ly/" or ".site/" or ".me/" or ".bg/"):
                            r = Domain(r)
                            r.addServerInfo()
                            r.checkDBForDomain()
                            
        i = i + 1
        
    else:
        sys.exit("All done!")


mainCrawler()