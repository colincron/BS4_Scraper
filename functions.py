from datetime import datetime
import random
import psycopg2
from config import secret

def writeToDB(urlToSave, table, column):
    conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = secret,
                            port = 5432)
    cur = conn.cursor()
    urlToSave = str(urlToSave)
    sql = "INSERT INTO {} ({}) VALUES ('{}');".format(table, column, urlToSave)
    try:
        with  conn.cursor() as cur:
            cur.execute(sql, (table))
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        cur.close()
        conn.close()
        print(error)
    cur.close()
    conn.close()
    return 0

def tstamp(): 
    dt = datetime.now()
    ts = dt.strftime("%H:%M:%S")
    return ts

def onionHandler(url):
    if url.endswith(".onion"):
        print("\n" + tstamp() + "Onion detected\n")
        writeToDB(url, "onions", "url")
        return url
    
def createRequestHeader():
    choice = random.randint(1, 3)
    if choice == 1:
        #Mac OS X-based computer using a Firefox browser
        header = {"Accept" : "text/html",
                "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
                "Accept-Encoding" : "gzip, deflate, br",
                "Referer" : "127.0.0.1"}
        return header
    elif choice == 2:
        #Chrome OS-based laptop using Chrome browser (Chromebook)
        header = {"Accept" : "text/html",
                "User-Agent" : "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
                "Accept-Encoding" : "gzip, deflate, br",
                "Referer" : "127.0.0.1"}
        return header
    elif choice == 3:
        #Windows 7-based PC using a Chrome browser
        header = {"Accept" : "text/html",
                "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
                "Accept-Encoding" : "gzip, deflate, br",
                "Referer" : "127.0.0.1"}
        return header

def printError(error):
    print("\n" + tstamp() + " " + str(error))
    
