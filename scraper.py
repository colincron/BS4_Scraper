import requests
from bs4 import BeautifulSoup
from functions import onionHandler
from classes import Domain
import threading

def mainCrawler():
    startUrl = input("Start URL: ")
    numberOfCrawls = input("How many crawls do you want to do? ")
    #databaseCreate = input("Do you need to create a database?")
    i = 0
    urlList = [startUrl,]

    while len(urlList) > i and int(numberOfCrawls) >= i: 
        url = urlList[i]
        print("\nLength of urlList: " + str(len(urlList)))
        print("Number of sites crawled:" + str(i) + "\n")
        
        while url.endswith("onion") or url.endswith("onion/"):
            onionHandler(url)
            url = urlList[ i + 1 ]
            i = i + 1
        
        print("Now scanning: " + url)
        
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            print("Connection refused")
        
        htmlData = response.content
        parsedData = BeautifulSoup(htmlData, "lxml") #lxml is fast and lenient
        anchors = parsedData.find_all(lambda tag: tag.name == 'a' and tag.get('href'))

        for a in anchors:
            references = [a["href"]]
            for r in references:
                if r.startswith("http") and r not in urlList:
                    urlList.append(r)
                    if r.endswith(".com/" or ".net/" or ".edu/" or ".org/"):
                        r = Domain(r)
                        r.writeToDatabase("domains")
                        print("\nDomain " + r.name + " written to DB\n")
        i = i + 1
        
    else:
        print("All done!")

if __name__ =="__main__":
    t1 = threading.Thread(target=mainCrawler)
    t2 = threading.Thread(target=mainCrawler)
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
 
    print("Done!")