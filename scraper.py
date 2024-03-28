import socket, sys, requests
from bs4 import BeautifulSoup
from classes import Domain
from functions import onionHandler, tstamp, createRequestHeader, printError

def mainCrawler():
    response = ""
    startUrl = input(tstamp() + " Start URL: ")
    #numberOfCrawls = input(tstamp() + " How many crawls do you want to do? ")
    numberOfCrawls = 5000
    urlList = [startUrl,]
    i = 0

    while len(urlList) > 0: 
        url = urlList[0]
        print("\n" + tstamp() + " Length of urlList: " + str(len(urlList)))
        print(tstamp() + " Number of sites crawled:" + str(i) + "\n")
        
        while url.endswith("onion") or url.endswith("onion/"):
            onionHandler(url)
            urlList.pop(0)
            i = i+1
        
        print(tstamp() + " Now scanning: " + url)
        
        header = createRequestHeader()
        
        try:
            response = requests.get(url, headers=header)
        except (requests.exceptions.ConnectionError, socket.gaierror, 
                requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL, 
                requests.exceptions.ChunkedEncodingError, requests.exceptions.InvalidSchema) as error:
            printError("\n" + tstamp() + " " + str(error))      
            
        if response:
            htmlData = response.content
            parsedData = BeautifulSoup(htmlData, "lxml") #lxml is fast and lenient
            anchors = parsedData.find_all(lambda tag: tag.name == 'a' and tag.get('href'))

            for a in anchors:
                references = [a["href"]]
                
                for r in references:
                    
                    if r.startswith("http") and r not in urlList:
                        urlList.append(r)
                        
                        if r.endswith(".com/" or ".net/" or ".edu/" or ".org/" or ".io/" or ".gov/" or ".co/" or ".uk/" or ".us/" or
                                        ".ai/" or ".io/" or ".info/" or ".xyz/" or ".ly/" or ".site/" or ".me/" or ".bg/" or ".hk/"):
                            d = Domain(r)
                            d.addServerInfo()
                            d.checkDBForDomain()
                            
                        elif r.endswith(".txt"):
                            print("\n\n" + tstamp() + " .txt found! Time to write more code!\n\n")
                            
        urlList.pop(0)
        i = i + 1
        
    else:
        sys.exit("All done!")

mainCrawler()