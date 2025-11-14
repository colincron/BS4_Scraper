import sqlite3, re, random, sys
from datetime import datetime
from bs4 import BeautifulSoup
import socket, requests


def timestamp():
    dt = datetime.now()
    ts = dt.strftime("%H:%M:%S")
    return ts


def print_error(error):
    print("\n" + timestamp() + " " + str(error))


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


def create_request_header():
    choice = random.randint(1, 3)
    if choice == 1:
        #Mac OS X-based computer using a Firefox browser
        header = {"Accept": "text/html",
                  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Referer": "127.0.0.1"}
        return header
    elif choice == 2:
        #Chrome OS-based laptop using Chrome browser (Chromebook)
        header = {"Accept": "text/html",
                  "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Referer": "127.0.0.1"}
        return header
    elif choice == 3:
        #Windows 7-based PC using a Chrome browser
        header = {"Accept": "text/html",
                  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Referer": "127.0.0.1"}
        return header


def email_scraper(response):
    try:
        # response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        emails = set()
        for link in soup.find_all('a', href=True):
            if 'mailto:' in link['href']:
                email = link['href'].replace('mailto:', '').strip()
                emails.add(email)

        # Method 2: Search in all text content AND attributes
        for tag in soup.find_all(True):
            # Check tag text
            if tag.string:
                found_emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[com]+', tag.string)
                emails.update(found_emails)

            # Check all attributes
            for attr_value in tag.attrs.values():
                if isinstance(attr_value, str):
                    found_emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[com]+', attr_value)
                    emails.update(found_emails)

        # Method 3: Search the raw HTML (most comprehensive)
        all_emails = set(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[com]+', response.text))
        emails.update(all_emails)

        for email in emails:
            print("Found email: " + email)
            # file1 = open("emails.txt", "a")
            # file1.write(email + "\n")
            # file1.close()
            write_to_email_database(email)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.TooManyRedirects) as err:
        print_error(err)


def request_and_parse(url):
    response = ""
    try:
        response = requests.get(url, headers=create_request_header())
    except (requests.exceptions.ConnectionError, socket.gaierror,
            requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL,
            requests.exceptions.ChunkedEncodingError, requests.exceptions.InvalidSchema) as error:
        print_error("\n" + timestamp() + " " + str(error))

    if response:
        html_data = response.content
        parsed_data = BeautifulSoup(html_data, "lxml")  # lxml is fast and lenient
        anchors = parsed_data.find_all(lambda tag: tag.name == 'a' and tag.get('href'))
        email_scraper(response)
        return anchors
    return None


def grab_title(url):
    get_response = ""
    try:
        get_response = requests.get(url, headers=create_request_header())
    except (requests.exceptions.TooManyRedirects, requests.exceptions.ConnectionError,
            socket.gaierror, requests.exceptions.InvalidURL) as error:
        print_error(str(error))

    if get_response:
        html_data = get_response.content
        parsed_data = BeautifulSoup(html_data, "lxml")  # lxml is fast and lenient
        title = parsed_data.find('title')
        if title:
            title = str(title).removeprefix("<title>").removesuffix("</title>")
            return title
        return None
    return None


def get_server_info(domain_name):
    try:
        header_response = requests.head(domain_name, headers=create_request_header())

        title = grab_title(domain_name)
        server = header_response.headers['Server']
        content_type = header_response.headers['Content-Type']
        ip = socket.gethostbyname(sanitize_url(str(domain_name)))
        write_to_domain_database(str(domain_name), ip, server, content_type, title)
        return 0

    except (KeyError, TypeError,
            UnicodeEncodeError, socket.error,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidURL) as err:
        print_error(str(err))
        return 0


def get_domain_names(anchors, url_list):
    try:
        for a in anchors:
            references = [a["href"]]
            for r in references:
                if r.startswith("http") and r not in url_list:
                    url_list.append(r)
                    tld_list = (".com", ".gov/", ".net/", ".edu/", ".org/", ".io/", ".co.uk/", ".ie/", ".info/")
                    if r.endswith(tld_list):
                        get_server_info(r)
    except TypeError as err:
        print_error(str(err))
    return url_list


def create_db(conn, table_name):
    if table_name == "Domains":
        try:
            conn.execute('''CREATE TABLE IF NOT EXISTS '{}' (
                                        "url"	TEXT NOT NULL,
                                        "ip"	TEXT NOT NULL,
                                        "servertype"	TEXT,
                                        "content_type"  TEXT,
                                        "title"	TEXT
                                        )'''.format(table_name))
        except sqlite3.OperationalError as err:
            print_error(err)
    elif table_name == "Emails":
        try:
            conn.execute('''CREATE TABLE IF NOT EXISTS '{}' (
                                        "email_address"	TEXT NOT NULL
                                        )'''.format(table_name))
        except sqlite3.OperationalError as err:
            print_error(err)


def check_db_for_domain(conn, name, table_name):
    db_result = ""
    print(timestamp() + " Checking for " + name + " in database")
    if table_name == "Domains":
        entry_exists = conn.execute("SELECT DISTINCT url FROM '{}' WHERE url='{}'".format(table_name, name))
        try:
            db_result = str(entry_exists.fetchall()[0]).replace("('", "").replace("',)", "")
        except IndexError as err:
            return True
        if db_result == name:
            print("\n" + timestamp() + " " + name + " is already in DB")
            return False
        else:
            return True
    elif table_name == "Emails":
        entry_exists = conn.execute("SELECT DISTINCT email_address FROM '{}' WHERE email_address='{}'".format(table_name, name))
        try:
            db_result = str(entry_exists.fetchall()[0]).replace("('", "").replace("',)", "")
        except IndexError as err:
            return True
        if db_result == name:
            print("\n" + timestamp() + " " + name + " is already in DB")
            return False
        else:
            return True


def write_to_domain_database(name, ip, server, content_type, title):
    table_name = "Domains"
    conn = sqlite3.connect("ScrapeDB", isolation_level=None)
    create_db(conn, table_name)
    if check_db_for_domain(conn, name, table_name):
        sql = """INSERT INTO '{}' (url, ip, servertype, content_type, title)
                    VALUES ('{}','{}','{}','{}','{}');""".format(table_name, name, ip, server, content_type, title)
        try:
            conn.execute(sql)
            print(timestamp() + " " + name + " saved to database")
            return
        finally:
            return
    return


def write_to_email_database(email_address):
    table_name = "Emails"
    conn = sqlite3.connect("ScrapeDB", isolation_level=None)
    create_db(conn, table_name)
    if check_db_for_domain(conn, email_address, table_name):
        sql = """INSERT INTO '{}' (email_address)
                    VALUES ('{}');""".format(table_name, email_address)
        try:
            conn.execute(sql)
            print(timestamp() + " " + email_address + " saved to database")
            return
        finally:
            return 0
    return 0


def main_crawler(start_url):
    url_list = [start_url, ]
    i = 0

    while len(url_list) > 0:
        url = url_list[0]
        print("\n" + timestamp() + " Length of url_list: " + str(len(url_list)))
        print(timestamp() + " Number of sites crawled:" + str(i) + "\n")
        print(timestamp() + " Now searching: " + url)

        anchors = request_and_parse(url)
        url_list = get_domain_names(anchors, url_list)
        url_list.pop(0)
        i = i + 1

    else:
        sys.exit(timestamp() + " All done!")
