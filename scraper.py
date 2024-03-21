import requests
from bs4 import BeautifulSoup
from dbfunctions import writeToDB#, deleteDBDupes
from functions import onionHandler, domainScout


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
                writeToDB(r, "webpages", "url")
                if r.endswith(".com/") or r.endswith(".edu/") or r.endswith(".org/"):
                    writeToDB(r, "domains", "url")
                    print("\nDomain written to DB\n")
                    print("attempting to port scan")
                    domainScout(r)
                    #deleteDBDupes()
    i = i + 1
    
else:
    print("All done!")
