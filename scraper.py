import socket, sys, requests
from bs4 import BeautifulSoup
from classes import Domain
from functions import onionHandler, tstamp, createRequestHeader, printError

def mainCrawler():
    response = ""
    start_url = input(tstamp() + " Start URL: ")
    #numberOfCrawls = input(tstamp() + " How many crawls do you want to do? ")
    number_of_crawls = 5000
    url_list = [start_url,]
    print("URL List: " + str(url_list))
    i = 0

    while len(url_list) > 0:
        url = url_list[0]
        print("\n" + tstamp() + " Length of url_list: " + str(len(url_list)))
        print(tstamp() + " Number of sites crawled:" + str(i) + "\n")
        
        while url.endswith("onion") or url.endswith("onion/"):
            onionHandler(url)
            url_list.pop(0)
            i = i+1
        
        print(tstamp() + " Now searching: " + url)
        
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
                    
                    if r.startswith("http") and r not in url_list:
                        url_list.append(r)
                        tldList = (".com",".gov/",".net/",".edu/",".org/",".io/",".co.uk/",".ie/",".info/")
                        if r.endswith(tldList):
                            d = Domain(r)
                            print(d.name)
                            d.addServerInfo()
                            d.check_db_for_domain()
                            #d.write_to_database("Scraped")
                        elif r.endswith(".txt"):
                            print("\n\n" + tstamp() + " .txt found! Time to write more code!\n\n")
                            
        url_list.pop(0)
        i = i + 1
        
    else:
        sys.exit("All done!")

mainCrawler()