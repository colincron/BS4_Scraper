import psycopg2
from config import secret
import socket
import requests
from functions import tstamp, printError


class Domain:
    
    name = ""
    ip = ""
    server = ""
    xframe = ""
    
    def __init__(self, name):
        self.name = name
        #print(tstamp() + " self.name = " + self.name)
        return
        
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
        # returns IPV4 address
        return target
    
    def addServerInfo(self):
        url = self.name
        try: 
            response = requests.head(url)
            server = response.headers['Server']
            xframe = response.headers['X-Frame-Options']
            self.server = server
            self.xframe = xframe
        except KeyError as error:
            printError(error)
            return 0
        except requests.exceptions.ConnectionError as error:
            printError(error)
            return 0
        except socket.gaierror as error:
            print("\n" + tstamp() + " " + error)
            return 0
        
    def writeToDatabase(self, table):
        conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = secret,
                            port = 5432)
        cur = conn.cursor()
        #urlToSave = str(urlToSave)
        sql = "INSERT INTO {} (url, ip, servertype, xframe) VALUES ('{}','{}','{}','{}');".format(table, self.name, self.ip, self.server, self.xframe)
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
                        print("\n" + tstamp() +" Dupe found!\n")
                        return
                except:
                    self.writeToDatabase("domains")
                    return
                
        except (Exception, psycopg2.DatabaseError) as error:
            cur.close()
            conn.close()
            print(error) 
        cur.close()
        conn.close()
        return