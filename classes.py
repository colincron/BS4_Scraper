import socket, requests
from bs4 import BeautifulSoup
from functions import timestamp, print_error, create_request_header, create_db, sanitize_url
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
        
    def add_title(self):
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
        try:
            self.ip = socket.gethostbyname(sanitize_url(str(self.name)))
        except socket.error as err:
            print(timestamp() + " Error: " + str(err))
            return 0
        except TypeError as err:
            print(timestamp() + " Error: " + str(err))
            return 0
    def add_server_info(self):
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
        
        self.add_title()
        print(timestamp() + " Title: " + self.title)

    def write_to_database(self, table):
        conn = sqlite3.connect("ScrapeDB", isolation_level=None)
        create_db(conn)
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

        print(timestamp() + " Checking for duplicate URL in database")
        entry_exists = conn.execute("SELECT DISTINCT url FROM Scraped WHERE url='{}'".format(self.name))
        if entry_exists == self.name:
            print(timestamp() + " URL already in DB")
            return
        else:
            self.write_to_database("Scraped")
            print(timestamp() + " URL written to DB")
            return
