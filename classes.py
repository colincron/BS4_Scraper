import psycopg2, socket, requests
from config import secret
from urllib.request import urlopen
from bs4 import BeautifulSoup
from functions import tstamp, printError, createRequestHeader

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
            except:
                return 0
        elif self.name.startswith("http") is True:
            try:
                self.name = (self.name.removeprefix("http://")).removesuffix("/")
                print(tstamp() + " Self.name: " + self.name)
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
    
    def writeToDatabase(self, table):
        conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = secret,
                            port = 5432)
        cur = conn.cursor()
        #urlToSave = str(urlToSave)
        sql = """INSERT INTO {} (url, ip, servertype, xframe, title) 
            VALUES ('{}','{}','{}','{}','{}');""".format(table, self.name, 
            self.ip, self.server, self.xframe, self.title)
        try:
            with  conn.cursor() as cur:
                cur.execute(sql, (table))
                conn.commit()
                print(tstamp() + " Written to DB: " + self.name)
        except (Exception, psycopg2.DatabaseError) as error:
            cur.close()
            conn.close()
            print(error)
        cur.close()
        conn.close()
        return 0
    
    def checkDBForDomain(self):
        self.ip = self.addIP()
        conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = secret,
                            port = 5432)
        cur = conn.cursor()
        sql = "SELECT url from domains where url @@ to_tsquery('{}');".format(self.name)
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()
                conn.commit()
                try: 
                    if str(*result[0]) == self.name:
                        return True
                except:
                    self.writeToDatabase("domains")
                    return False
                
        except (Exception, psycopg2.DatabaseError) as error:
            cur.close()
            conn.close()
            print("\n" + tstamp() + " " + str(error)) 
        cur.close()
        conn.close()
        return