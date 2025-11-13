import socket, requests
from bs4 import BeautifulSoup
from functions import tstamp, printError, createRequestHeader
from scanner import scanner
import sqlite3


class Domain:
    
    name = ""
    ip = ""
    server = ""
    xframe = ""
    title = ""
    
    def __init__(self, name):
        self.name = name
        #print(tstamp() + " self.name = " + self.name)
        return
        
    def addTitle(self):
        response = ""
        url = self.name
        header = createRequestHeader()
        try:
            response = requests.get(url, headers=header)
        except (requests.exceptions.TooManyRedirects, requests.exceptions.ConnectionError, 
                socket.gaierror, requests.exceptions.InvalidURL) as error:
            printError("\n" + tstamp() + " " + str(error))

        if response:
            htmlData = response.content
            parsedData = BeautifulSoup(htmlData, "lxml") #lxml is fast and lenient
            title = parsedData.find('title')
            if title:
                title = str(title).removeprefix("<title>").removesuffix("</title>")
                self.title = title
        
    def addIP(self):
        target = ""
        if self.name.startswith("https") is True:
            try:
                self.name = (self.name.removeprefix("https://")).removesuffix("/")
                target = socket.gethostbyname(self.name)
                try:
                    print("port scanning")
                    scanner(self.name)
                except:
                    return target
            except:
                return 0
        elif self.name.startswith("http") is True:
            try:
                self.name = (self.name.removeprefix("http://")).removesuffix("/")
                print(tstamp() + " Self.name: " + self.name)
                try:
                    scanner(self.name)
                except:
                    return target
            except:
                print(tstamp() + " Not this time.")
            try:
                target = socket.gethostbyname(str(self.name)) 
            except socket.gaierror as error:
                printError(error)
        return target
    
    def addServerInfo(self):
        url = self.name
        try: 
            response = requests.head(url)
            self.server = response.headers['Server']
            self.xframe = response.headers['X-Frame-Options']
        except KeyError as error:
            printError("\n" + tstamp() + " " + str(error))
            return 0
        except socket.gaierror as error:
            printError("\n" + tstamp() + " " + str(error))
            return 0
        except requests.exceptions.ConnectionError as error:
            printError("\n" + tstamp() + " " + str(error))
            return 0
        except requests.exceptions.SSLError as error:
            printError("\n" + tstamp() + " " + str(error))
            return 0
        except requests.exceptions.InvalidURL as error:
            printError("\n" + tstamp() + " " + str(error))
        
        self.addTitle()
        print("Title: " + self.title)
        try:
            print("port scanning")
            scanner(self.name)
        except:
            return 0

    def write_to_database(self, table):
        conn = sqlite3.connect("ScrapeDB", isolation_level=None)
        # print("Connected to DB")
        conn.execute('''CREATE TABLE IF NOT EXISTS "Scraped" (
                            "url"	TEXT NOT NULL,
                	        "ip"	TEXT NOT NULL,
                	        "servertype"	TEXT,
                	        "xframe"	TEXT,
                	        "title"	TEXT
                            )''')
        sql = """INSERT INTO {} (url, ip, servertype, xframe, title)
                    VALUES ('{}','{}','{}','{}','{}');""".format(table, self.name,
                                                                 self.ip, self.server, self.xframe, self.title)
        try:
            conn.execute(sql)
            # print("sent info to DB")
            return
        finally:
            return 0
        return

    def check_db_for_domain(self):
        conn = sqlite3.connect('ScrapeDB', isolation_level=None)
        # print("Connected to DB")
        entry_exists = conn.execute("SELECT DISTINCT url FROM Scraped WHERE url='{}'".format(self.name))
        if entry_exists == self.name:
            print("URL already in DB")
            return
        else:
            self.write_to_database("Scraped")
            print("URL written to DB")
            return
