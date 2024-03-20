import requests
from bs4 import BeautifulSoup

startUrl = input("Start URL: ")
i = 0
urlList = [startUrl,]

while len(urlList) > 0: 
    url = urlList[i]
    print(url)
    print("Length of urlList: " + str(len(urlList)))
    i = i + 1
    
    response = requests.get(url, headers = headers)
    htmlData = response.content
    parsedData = BeautifulSoup(htmlData, "lxml") #lxml is fast and lenient
    anchors = parsedData.find_all("a")
    
    for a in anchors:
        #print(a)
        references = [a["href"]]
        for r in references:
            if r.startswith("http"):
                #print(r)
                urlList.append(r)
                set(urlList) #order of list elements possibly lost by conversion, but duplicates removed
                list(urlList)