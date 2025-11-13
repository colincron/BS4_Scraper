import socket, sys, requests
from bs4 import BeautifulSoup
from classes import Domain
from functions import timestamp, create_request_header, print_error

def main_crawler():
    response = ""
    start_url = input(timestamp() + " Start URL: ")
    url_list = [start_url,]
    print("URL List: " + str(url_list))
    i = 0

    while len(url_list) > 0:
        url = url_list[0]
        print("\n" + timestamp() + " Length of url_list: " + str(len(url_list)))
        print(timestamp() + " Number of sites crawled:" + str(i) + "\n")
        print(timestamp() + " Now searching: " + url)
        
        header = create_request_header()
        
        try:
            response = requests.get(url, headers=header)
        except (requests.exceptions.ConnectionError, socket.gaierror, 
                requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL, 
                requests.exceptions.ChunkedEncodingError, requests.exceptions.InvalidSchema) as error:
            print_error("\n" + timestamp() + " " + str(error))
            
        if response:
            html_data = response.content
            parsed_data = BeautifulSoup(html_data, "lxml") #lxml is fast and lenient
            anchors = parsed_data.find_all(lambda tag: tag.name == 'a' and tag.get('href'))

            for a in anchors:
                references = [a["href"]]
                
                for r in references:
                    
                    if r.startswith("http") and r not in url_list:
                        url_list.append(r)
                        tld_list = (".com",".gov/",".net/",".edu/",".org/",".io/",".co.uk/",".ie/",".info/")
                        if r.endswith(tld_list):
                            d = Domain(r)
                            print(d.name)
                            d.addServerInfo()
                            d.get_ip_address()
                            d.check_db_for_domain()
                        elif r.endswith(".txt"):
                            print("\n\n" + timestamp() + " .txt found! Time to write more code!\n\n")
                            # TODO
                            # write a handler for .txt files and other interesting file types
                            
        url_list.pop(0)
        i = i + 1
        
    else:
        sys.exit("All done!")

main_crawler()