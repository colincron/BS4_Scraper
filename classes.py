import psycopg2
from config import secret
import socket


class Domain:
    
    name = ""
    ip = ""
    
    def __init__(self, name):
        self.name = name
        print("self.name = " + self.name)
        return
        
    def addIP(self):
        target = ""
        if self.name.startswith("https") is True:
            try:
                self.name = (self.name.removeprefix("https://")).removesuffix("/")
                print("https removed = " + self.name)
                target = socket.gethostbyname(self.name)
            except:
                print("Not this time.")
        elif self.name.startswith("http") is True:
            try:
                self.name = (self.name.removeprefix("http://")).removesuffix("/")
                print("http removed")
                print("This has no https-> "+ self.name)
                print("Self.name: " + self.name)
            except:
                print("Not this time.")
            try:
                target = socket.gethostbyname(str(self.name)) 
            except socket.gaierror:
                print("gaierror :(")
        # returns IPV4 address
        return target
    
    def writeToDatabase(self, table):
        self.ip = self.addIP()
        conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = secret,
                            port = 5432)
        cur = conn.cursor()
        #urlToSave = str(urlToSave)
        sql = "INSERT INTO {} (url, ip) VALUES ('{}','{}');".format(table, self.name, self.ip)
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
            
