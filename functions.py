from datetime import datetime
import random
import requests
from bs4 import BeautifulSoup


def sanitize_url(url):
    sanitized = ""
    if url.startswith("https://") and url.endswith("/"):
        sanitized = url.replace("https://", "")
        sanitized = sanitized[:-1]
    elif url.startswith("http://") and url.endswith("/"):
        sanitized = url.replace("https://", "")
        sanitized = sanitized[:-1]
    elif url.startswith("https://"):
        sanitized = url.replace("https://", "")
    elif url.startswith("http://"):
        sanitized = url.replace("http://", "")
    return sanitized

def create_db(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS "Scraped" (
                                "url"	TEXT NOT NULL,
                    	        "ip"	TEXT NOT NULL,
                    	        "servertype"	TEXT,
                    	        "cache_control" TEXT,
                    	        "xframe"	TEXT,
                    	        "content_type"  TEXT,
                    	        "title"	TEXT
                                )''')

def timestamp():
    dt = datetime.now()
    ts = dt.strftime("%H:%M:%S")
    return ts
    
def create_request_header():
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

def print_error(error):
    print("\n" + timestamp() + " " + str(error))
    
def request_function(url):
    response = ""
    header = create_request_header()
    try:
        response = requests.get(url, headers=header)
    except (requests.exceptions.ConnectionError, socket.gaierror,
            requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL,
            requests.exceptions.ChunkedEncodingError, requests.exceptions.InvalidSchema) as error:
        print_error("\n" + timestamp() + " " + str(error))

    if response:
        html_data = response.content
        parsed_data = BeautifulSoup(html_data, "lxml")  # lxml is fast and lenient
        anchors = parsed_data.find_all(lambda tag: tag.name == 'a' and tag.get('href'))
        return anchors
    return 0
