import requests
from bs4 import BeautifulSoup

i = 0
urlList = ["https://www.kdnuggets.com/2023/04/stepbystep-guide-web-scraping-python-beautiful-soup.html/",]

while len(urlList) > 0: 
    url = urlList[i]
    print(url)
    print("Length of urlList: " + str(len(urlList)))
    i = i + 1
    
    response = requests.get(url)
    htmlData = response.content
    parsedData = BeautifulSoup(htmlData, "lxml") #lxml is fast and lenient
    #print(parsedData.prettify())
    anchors = parsedData.find_all("a")
    
    for a in anchors:
        #print(a)
        references = [a["href"]]
        for r in references:
            if r.startswith("http") is True:
                #print(r)
                urlList.append(r)
                set(urlList) #order of list elements lost by conversion, but duplicates removed
                list(urlList)
    
    if i > 5:
        print(urlList)
        break
