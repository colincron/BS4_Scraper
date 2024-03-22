import psycopg2
from secret_file import pword
import socket


class Domain:
    
    name = ""
    ip = ""
    
    def __init__(self, name):
        self.name = name
        print("self.name = " + self.name)
        return
        
    def addIP(self):
        if self.name.startswith("https") is True:
            self.name = (self.name.removeprefix("https://")).removesuffix("/")
            print("https removed = " + self.name)
            target = socket.gethostbyname(self.name) 
        elif self.name.startswith("http") is True:
            self.name = (self.name.removeprefix("http://")).removesuffix("/")
            print("http removed")
            print("This has no http/s-> "+ self.name)
            print("Self.name " + self.name)
            target = socket.gethostbyname(self.name) 
        # returns IPV4 address
        return target
    
 
    
    def writeToDatabase(self, table):
        self.ip = self.addIP()
        conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = pword,
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
            
