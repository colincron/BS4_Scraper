import psycopg2
from config import secret
import socket
import requests
from functions import tstamp 


class Domain:
    
    name = ""
    ip = ""
    server = ""
    
    def __init__(self, name):
        self.name = name
        print(tstamp() + " self.name = " + self.name)
        return
        
    def addIP(self):
        target = ""
        if self.name.startswith("https") is True:
            try:
                self.name = (self.name.removeprefix("https://")).removesuffix("/")
                print(tstamp() + " https removed = " + self.name)
                target = socket.gethostbyname(self.name)
            except:
                print(tstamp() + " Not this time.")
        elif self.name.startswith("http") is True:
            try:
                self.name = (self.name.removeprefix("http://")).removesuffix("/")
                print(tstamp() + " http removed")
                print(tstamp() + " This has no https-> "+ self.name)
                print(tstamp() + " Self.name: " + self.name)
            except:
                print(tstamp() + " Not this time.")
            try:
                target = socket.gethostbyname(str(self.name)) 
            except socket.gaierror:
                print(tstamp() + " gaierror :(")
        # returns IPV4 address
        return target
    
    def addServerInfo(self):
        url = self.name
        try: 
            response = requests.head(url)
            server = response.headers['Server']
            print(tstamp() + " Server: " + server)
            self.server = server
            return server
        except KeyError:
            print(" \n" + tstamp() + "Key Error!\n")
            return 0
        except requests.exceptions.ConnectionError:
            print(" \n" + tstamp() + "Host refused connection. Probably too many retries\n")
            return 0
        except socket.gaierror:
            print("\n" + tstamp() + "Gai Error\n")
            return 0
        
    def writeToDatabase(self, table):
        self.ip = self.addIP()
        conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = secret,
                            port = 5432)
        cur = conn.cursor()
        #urlToSave = str(urlToSave)
        sql = "INSERT INTO {} (url, ip, servertype) VALUES ('{}','{}','{}');".format(table, self.name, self.ip, self.server)
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
            
