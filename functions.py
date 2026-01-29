import sqlite3, re, random, sys, socket, asyncio
from datetime import datetime
from urllib.parse import urlparse, urljoin, urlunparse, parse_qs
from bs4 import BeautifulSoup
import aiohttp
import hashlib


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
        sanitized = url.replace("http://", "")
        sanitized = sanitized[:-1]
    elif url.startswith("https://"):
        sanitized = url.replace("https://", "")
    elif url.startswith("http://"):
        sanitized = url.replace("http://", "")
    return sanitized


def normalize_url(url):
    try:
        parsed = urlparse(url)
        normalized = urlunparse((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip('/') if parsed.path != '/' else '/',
            parsed.params,
            parsed.query,
            ''
        ))
        return normalized
    except:
        return url


def url_hash(url):
    return hashlib.md5(normalize_url(url).encode()).hexdigest()


def create_request_header():
    choice = random.randint(1, 3)
    if choice == 1:
        header = {"Accept": "text/html",
                  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Referer": "127.0.0.1"}
        return header
    elif choice == 2:
        header = {"Accept": "text/html",
                  "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Referer": "127.0.0.1"}
        return header
    elif choice == 3:
        header = {"Accept": "text/html",
                  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Referer": "127.0.0.1"}
        return header
    return None


def detect_vulnerabilities(url, html_content):
    vulnerabilities = []
    
    sql_injection_patterns = [
        (r"union\s+select", "SQL Injection - UNION SELECT", "high"),
        (r"(\'|\")(\s+)?(or|OR)(\s+)?(\'|\")?(1|true)", "SQL Injection - OR statement", "high"),
        (r"(insert|delete|drop|update)\s+into", "SQL Injection - Data manipulation", "high"),
        (r"(;|--|\#|\/\*)", "SQL Injection - Comment injection", "medium"),
    ]
    
    xss_patterns = [
        (r"<script[^>]*>", "XSS - Script tag", "high"),
        (r"on(load|error|click|mouse\w+)\s*=", "XSS - Event handler", "high"),
        (r"javascript:", "XSS - JavaScript URI", "high"),
        (r"<iframe[^>]*>", "XSS - Iframe injection", "medium"),
        (r"eval\s*\(", "XSS - Eval usage", "medium"),
    ]
    
    open_redirect_params = ["redirect", "url", "goto", "next", "return", "returnUrl", "target", "dest", "destination"]
    lfi_patterns = [
        (r"\.\./", "LFI - Path traversal", "high"),
        (r"(file|path|dir|folder)=", "LFI - File parameter", "medium"),
    ]
    
    ssrf_patterns = [
        (r"(localhost|127\.0\.0\.1)", "SSRF - Localhost reference", "high"),
        (r"(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)", "SSRF - Private IP", "high"),
        (r"(url|target|dest|api)=", "SSRF - URL parameter", "medium"),
    ]
    
    sensitive_file_patterns = [
        (r"\.env", "Exposed .env file", "high"),
        (r"\.git/", "Exposed .git directory", "high"),
        (r"\.aws/", "Exposed AWS credentials", "high"),
        (r"config\.(php|ini|yml|yaml|json)", "Exposed config file", "high"),
        (r"(web|application|app)\.config", "Exposed config file", "high"),
        (r"backup\.(sql|zip|tar|gz)", "Exposed backup file", "medium"),
        (r"phpinfo\.php", "Exposed phpinfo", "medium"),
    ]
    
    default_creds_patterns = [
        (r"(admin|root|user):?(admin|password|123456|root)", "Default credentials", "high"),
        (r"(username|user|login)=(admin|root|test)", "Default username", "medium"),
    ]
    
    url_lower = url.lower()
    content_lower = html_content.lower() if html_content else ""
    
    for pattern, vuln_type, severity in sql_injection_patterns:
        if re.search(pattern, url_lower, re.IGNORECASE) or (html_content and re.search(pattern, content_lower, re.IGNORECASE)):
            vulnerabilities.append({
                "url": url,
                "type": vuln_type,
                "severity": severity,
                "pattern": pattern,
                "details": f"Found pattern: {pattern}"
            })
    
    for pattern, vuln_type, severity in xss_patterns:
        if re.search(pattern, url_lower, re.IGNORECASE) or (html_content and re.search(pattern, content_lower, re.IGNORECASE)):
            vulnerabilities.append({
                "url": url,
                "type": vuln_type,
                "severity": severity,
                "pattern": pattern,
                "details": f"Found pattern: {pattern}"
            })
    
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    for param in open_redirect_params:
        if param in query_params:
            vulnerabilities.append({
                "url": url,
                "type": "Open Redirect",
                "severity": "medium",
                "pattern": f"?{param}=",
                "details": f"Potential open redirect via parameter: {param}"
            })
    
    for pattern, vuln_type, severity in lfi_patterns:
        if re.search(pattern, url_lower, re.IGNORECASE):
            vulnerabilities.append({
                "url": url,
                "type": vuln_type,
                "severity": severity,
                "pattern": pattern,
                "details": f"Found pattern: {pattern}"
            })
    
    for pattern, vuln_type, severity in ssrf_patterns:
        if re.search(pattern, url_lower, re.IGNORECASE) or (html_content and re.search(pattern, content_lower, re.IGNORECASE)):
            vulnerabilities.append({
                "url": url,
                "type": vuln_type,
                "severity": severity,
                "pattern": pattern,
                "details": f"Found pattern: {pattern}"
            })
    
    for pattern, vuln_type, severity in sensitive_file_patterns:
        if re.search(pattern, url_lower, re.IGNORECASE):
            vulnerabilities.append({
                "url": url,
                "type": vuln_type,
                "severity": severity,
                "pattern": pattern,
                "details": f"Found pattern: {pattern}"
            })
    
    for pattern, vuln_type, severity in default_creds_patterns:
        if re.search(pattern, url_lower, re.IGNORECASE) or (html_content and re.search(pattern, content_lower, re.IGNORECASE)):
            vulnerabilities.append({
                "url": url,
                "type": vuln_type,
                "severity": severity,
                "pattern": pattern,
                "details": f"Found pattern: {pattern}"
            })
    
    return vulnerabilities


def email_scraper(html_content):
    email_pattern = r"[\w\-\.]+@([\w-]+\.)+[\w-]{2,}"
    emails = re.findall(email_pattern, html_content)
    if len(emails) > 0:
        for email in emails:
            write_to_email_database(email)


async def fetch_url(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, headers=create_request_header(), timeout=aiohttp.ClientTimeout(total=30), ssl=False) as response:
                html_content = await response.text()
                return url, html_content, response.status
        except Exception as error:
            print_error(f"Error fetching {url}: {str(error)}")
            return url, None, None


def extract_urls_from_html(html_content, base_url):
    urls = []
    try:
        parsed_data = BeautifulSoup(html_content, "lxml")
        
        anchors = parsed_data.find_all('a', href=True)
        for a in anchors:
            href = a['href']
            full_url = urljoin(base_url, href)
            if full_url.startswith('http'):
                urls.append(full_url)
        
        scripts = parsed_data.find_all('script', src=True)
        for script in scripts:
            src = script['src']
            full_url = urljoin(base_url, src)
            if full_url.startswith('http'):
                urls.append(full_url)
        
        script_tags = parsed_data.find_all('script')
        for script in script_tags:
            if script.string:
                js_urls = re.findall(r'["\']((https?://|/)[^\s"\']+)["\']', script.string)
                for url_match in js_urls:
                    js_url = url_match[0]
                    full_url = urljoin(base_url, js_url)
                    if full_url.startswith('http'):
                        urls.append(full_url)
        
    except Exception as e:
        print_error(f"Error parsing HTML: {str(e)}")
    
    return urls


async def grab_metadata_async(session, url, semaphore):
    async with semaphore:
        try:
            async with session.head(url, headers=create_request_header(), timeout=aiohttp.ClientTimeout(total=30), ssl=False, allow_redirects=True) as response:
                server = response.headers.get('Server', 'Unknown')
                content_type = response.headers.get('Content-Type', 'Unknown')
            
            async with session.get(url, headers=create_request_header(), timeout=aiohttp.ClientTimeout(total=30), ssl=False) as response:
                html = await response.text()
                parsed_data = BeautifulSoup(html, "lxml")
                title_tag = parsed_data.find('title')
                title = title_tag.get_text() if title_tag else 'No title'
            
            ip = socket.gethostbyname(sanitize_url(url))
            return url, ip, server, content_type, title
        except Exception as err:
            print_error(f"Error getting metadata for {url}: {str(err)}")
            return None


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
    elif table_name == "Vulnerabilities":
        try:
            conn.execute('''CREATE TABLE IF NOT EXISTS '{}' (
                                        "url"	TEXT NOT NULL,
                                        "vulnerability_type"	TEXT NOT NULL,
                                        "severity"	TEXT NOT NULL,
                                        "pattern"	TEXT,
                                        "details"	TEXT,
                                        "timestamp"	TEXT NOT NULL
                                        )'''.format(table_name))
        except sqlite3.OperationalError as err:
            print_error(err)


def check_db_for_domain(conn, name, table_name):
    print(timestamp() + " Checking for " + name + " in database")
    if table_name == "Domains":
        entry_exists = conn.execute("SELECT DISTINCT url FROM '{}' WHERE url=?".format(table_name), (name,))
        try:
            db_result = entry_exists.fetchone()
            if db_result:
                print("\n" + timestamp() + " " + name + " is already in DB")
                return False
        except IndexError:
            return True
        return True
    elif table_name == "Emails":
        entry_exists = conn.execute("SELECT DISTINCT email_address FROM '{}' WHERE email_address=?".format(table_name), (name,))
        try:
            db_result = entry_exists.fetchone()
            if db_result:
                print("\n" + timestamp() + " " + name + " is already in DB")
                return False
        except IndexError:
            return True
        return True
    return None


def write_to_domain_database(name, ip, server, content_type, title):
    table_name = "Domains"
    conn = sqlite3.connect("ScrapeDB", isolation_level=None)
    create_db(conn, table_name)
    if check_db_for_domain(conn, name, table_name):
        sql = """INSERT INTO '{}' (url, ip, servertype, content_type, title)
                    VALUES (?,?,?,?,?);""".format(table_name)
        try:
            conn.execute(sql, (name, ip, server, content_type, title))
            print(timestamp() + " " + name + " saved to database")
            return
        finally:
            conn.close()
            return
    conn.close()
    return


def write_to_email_database(email_address):
    table_name = "Emails"
    conn = sqlite3.connect("ScrapeDB", isolation_level=None)
    create_db(conn, table_name)
    if check_db_for_domain(conn, email_address, table_name):
        sql = """INSERT INTO '{}' (email_address)
                    VALUES (?);""".format(table_name)
        try:
            conn.execute(sql, (email_address,))
            print(timestamp() + " " + email_address + " saved to database")
        except sqlite3.OperationalError:
            pass
    conn.close()
    return


def write_vulnerability_to_db(vulnerability):
    table_name = "Vulnerabilities"
    conn = sqlite3.connect("ScrapeDB", isolation_level=None)
    create_db(conn, table_name)
    
    entry_exists = conn.execute(
        "SELECT * FROM '{}' WHERE url=? AND vulnerability_type=? AND pattern=?".format(table_name),
        (vulnerability['url'], vulnerability['type'], vulnerability['pattern'])
    )
    
    if not entry_exists.fetchone():
        sql = """INSERT INTO '{}' (url, vulnerability_type, severity, pattern, details, timestamp)
                    VALUES (?,?,?,?,?,?);""".format(table_name)
        try:
            conn.execute(sql, (
                vulnerability['url'],
                vulnerability['type'],
                vulnerability['severity'],
                vulnerability['pattern'],
                vulnerability['details'],
                timestamp()
            ))
            print(f"{timestamp()} [VULN] {vulnerability['severity'].upper()} - {vulnerability['type']} found at {vulnerability['url']}")
        except sqlite3.OperationalError as err:
            print_error(err)
    
    conn.close()


async def process_batch(session, urls, semaphore, url_list, visited_hashes):
    tasks = []
    for url in urls:
        tasks.append(fetch_url(session, url, semaphore))
    
    results = await asyncio.gather(*tasks)
    
    new_urls = []
    metadata_tasks = []
    
    for url, html_content, status in results:
        if html_content:
            email_scraper(html_content)
            
            vulnerabilities = detect_vulnerabilities(url, html_content)
            for vuln in vulnerabilities:
                write_vulnerability_to_db(vuln)
            
            extracted_urls = extract_urls_from_html(html_content, url)
            
            for new_url in extracted_urls:
                new_hash = url_hash(new_url)
                if new_hash not in visited_hashes and new_url not in url_list:
                    url_list.append(new_url)
                    new_urls.append(new_url)
                    visited_hashes.add(new_hash)
            
            parsed_url = urlparse(url)
            if parsed_url.path in ['', '/'] and parsed_url.query == '':
                metadata_tasks.append(grab_metadata_async(session, url, semaphore))
    
    if metadata_tasks:
        metadata_results = await asyncio.gather(*metadata_tasks)
        for result in metadata_results:
            if result:
                url, ip, server, content_type, title = result
                write_to_domain_database(url, ip, server, content_type, title)
    
    return new_urls


def main_crawler(start_url, concurrency=10):
    url_list = [start_url]
    visited_hashes = {url_hash(start_url)}
    i = 0
    
    async def run_crawler():
        nonlocal i
        semaphore = asyncio.Semaphore(concurrency)
        
        async with aiohttp.ClientSession() as session:
            while url_list:
                batch_size = min(concurrency, len(url_list))
                batch = url_list[:batch_size]
                
                print("\n" + timestamp() + " Length of url_list: " + str(len(url_list)))
                print(timestamp() + " Number of sites crawled: " + str(i))
                print(timestamp() + " Now processing batch of " + str(len(batch)) + " URLs\n")
                
                await process_batch(session, batch, semaphore, url_list, visited_hashes)
                
                for _ in range(len(batch)):
                    url_list.pop(0)
                
                i += len(batch)
                
                if i > 10000:
                    print(timestamp() + " Reached 10000 URLs limit")
                    break
        
        print(timestamp() + " All done!")
    
    asyncio.run(run_crawler())
