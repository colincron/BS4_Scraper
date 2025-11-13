import socket, requests
from bs4 import BeautifulSoup
from functions import timestamp, print_error, create_request_header, create_db
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
        header = create_request_header()
        try:
            response = requests.get(url, headers=header)
        except (requests.exceptions.TooManyRedirects, requests.exceptions.ConnectionError, 
                socket.gaierror, requests.exceptions.InvalidURL) as error:
            print_error("\n" + timestamp() + " " + str(error))

        if response:
            htmlData = response.content
            parsedData = BeautifulSoup(htmlData, "lxml") #lxml is fast and lenient
            title = parsedData.find('title')
            if title:
                title = str(title).removeprefix("<title>").removesuffix("</title>")
                self.title = title

    def get_ip_address(self):
        print("GET IP ADDRESS RUNNING")
        sanitized = ""
        if str(self.name).startswith("https://") and str(self.name).endswith("/"):
            print("First condition")
            sanitized = str(self.name).replace("https://", "")
            sanitized = sanitized[:-1]
        elif str(self.name).startswith("http://") and str(self.name).endswith("/"):
            print("Second condition")
            sanitized = str(self.name).replace("https://", "")
            sanitized = sanitized[:-1]
        elif str(self.name).startswith("https://"):
            print("third condition")
            sanitized = str(self.name).replace("https://", "")
            print(sanitized)
        elif str(self.name).startswith("http://"):
            print("final condition")
            sanitized = str(self.name).replace("http://", "")

        print("GETTING IP ADDY: " + sanitized)
        try:
            self.ip = socket.gethostbyname(sanitized)
        # if error occurs, returns the error
        except socket.error as err:
            print(f"Error: {err}")
    
    def addServerInfo(self):
        url = self.name
        try: 
            response = requests.head(url)
            self.server = response.headers['Server']
            self.xframe = response.headers['X-Frame-Options']
        except KeyError as error:
            print_error("\n" + timestamp() + " " + str(error))
            return 0
        except socket.gaierror as error:
            print_error("\n" + timestamp() + " " + str(error))
            return 0
        except requests.exceptions.ConnectionError as error:
            print_error("\n" + timestamp() + " " + str(error))
            return 0
        except requests.exceptions.SSLError as error:
            print_error("\n" + timestamp() + " " + str(error))
            return 0
        except requests.exceptions.InvalidURL as error:
            print_error("\n" + timestamp() + " " + str(error))
        
        self.addTitle()
        print("Title: " + self.title)

    def write_to_database(self, table):
        conn = sqlite3.connect("ScrapeDB", isolation_level=None)
        create_db(conn)
        # conn.execute('''CREATE TABLE IF NOT EXISTS "Scraped" (
        #                     "url"	TEXT NOT NULL,
        #         	        "ip"	TEXT NOT NULL,
        #         	        "servertype"	TEXT,
        #         	        "xframe"	TEXT,
        #         	        "title"	TEXT
        #                     )''')
        sql = """INSERT INTO {} (url, ip, servertype, xframe, title)
                    VALUES ('{}','{}','{}','{}','{}');""".format(table, self.name,
                                                                 self.ip, self.server, self.xframe, self.title)
        try:
            conn.execute(sql)
            return
        finally:
            return 0
        return

    def check_db_for_domain(self):
        conn = sqlite3.connect('ScrapeDB', isolation_level=None)
        create_db(conn)
        # conn.execute('''CREATE TABLE IF NOT EXISTS "Scraped" (
        #                             "url"	TEXT NOT NULL,
        #                 	        "ip"	TEXT NOT NULL,
        #                 	        "servertype"	TEXT,
        #                 	        "xframe"	TEXT,
        #                 	        "title"	TEXT
        #                             )''')
        print(timestamp() + " Checking for duplicate URL in database")
        entry_exists = conn.execute("SELECT DISTINCT url FROM Scraped WHERE url='{}'".format(self.name))
        if entry_exists == self.name:
            print(timestamp() + " URL already in DB")
            return
        else:
            self.write_to_database("Scraped")
            print(timestamp() + " URL written to DB")
            return
