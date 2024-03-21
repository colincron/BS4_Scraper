def onionFinder(url, i, listofurls):
    if url.endswith(".onion"):
        print("\nOnion detected\n")
        file = open('onionURLs.txt','a')
        file.write(url)
        file.close()
        url = listofurls[ i + 1 ]
        i = i + 1
        return url, i, listofurls