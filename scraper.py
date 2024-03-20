#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

startUrl = input("Start URL: ")
i = 0
urlList = [startUrl,]

while len(urlList) > 0: 
    url = urlList[i]
    #print(url)
    print("Length of urlList: " + str(len(urlList)) + "\n")
    print("Now scanning: " + url)
    i = i + 1
    
    response = requests.get(url)
    htmlData = response.content
    parsedData = BeautifulSoup(htmlData, "html.parser") #lxml is fast and lenient
    #anchors = parsedData.find_all("a")
    anchors = parsedData.find_all(lambda tag: tag.name == 'a' and tag.get('href'))
    
    file = open('urls.txt','a')
    for a in anchors:
        #print("A")
        #print(a)
        references = [a["href"]]
        for r in references:
            if r.startswith("http") and r not in urlList:
                #print("R")
                print(r + "\n")
                urlList.append(r)
                file.write(r+"\n")
                
