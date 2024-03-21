from dbfunctions import writeToDB

def onionFinder(url):
    if url.endswith(".onion"):
        print("\nOnion detected\n")
        writeToDB(url, "onions", "url")
        print("\n\n\nONION WRITTEN TO DB\n\n\n")
        
        return url