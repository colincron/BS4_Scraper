import requests
from bs4 import BeautifulSoup
from dbfunctions import writeToDB


startUrl = input("Start URL: ")
i = 0
urlList = [startUrl,]

while len(urlList) > 0: 
    url = urlList[i]
    print("Length of urlList: " + str(len(urlList)) + "\n")
    print("Now scanning: " + url)
    i = i + 1
    
    response = requests.get(url)
    htmlData = response.content
    parsedData = BeautifulSoup(htmlData, "lxml") #lxml is fast and lenient
    anchors = parsedData.find_all(lambda tag: tag.name == 'a' and tag.get('href'))
    
    file = open('urls.txt','a')
    for a in anchors:
        references = [a["href"]]
        for r in references:
            if r.startswith("http") and r not in urlList:
                print(r + "\n")
                urlList.append(r)
                file.write(r+"\n")
                writeToDB(r)
    if i == 2000:
        break
                
