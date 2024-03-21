from dbfunctions import writeToDB

def onionHandler(url):
    if url.endswith(".onion"):
        print("\nOnion detected\n")
        writeToDB(url, "onions", "url")
        return url