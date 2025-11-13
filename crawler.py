import sys
from classes import Domain
from functions import timestamp, request_and_parse


def main_crawler():
    start_url = input(timestamp() + " Start URL: ")
    url_list = [start_url,]
    print("URL List: " + str(url_list))
    i = 0

    while len(url_list) > 0:
        url = url_list[0]
        print("\n" + timestamp() + " Length of url_list: " + str(len(url_list)))
        print(timestamp() + " Number of sites crawled:" + str(i) + "\n")
        print(timestamp() + " Now searching: " + url)
        
        anchors = request_and_parse(url)
        for a in anchors:
            references = [a["href"]]

            for r in references:

                if r.startswith("http") and r not in url_list:
                    url_list.append(r)
                    tld_list = (".com",".gov/",".net/",".edu/",".org/",".io/",".co.uk/",".ie/",".info/")
                    if r.endswith(tld_list):
                        d = Domain(r)
                        print(d.name)
                        d.add_server_info()
                        d.get_ip_address()
                        d.check_db_for_domain()
                    elif r.endswith(".txt"):
                        print("\n\n" + timestamp() + " .txt found! Time to write more code!\n\n")
                        # TODO
                        # write a handler for .txt files and other interesting file types
                            
        url_list.pop(0)
        i = i + 1
        
    else:
        sys.exit(timestamp() + " All done!")

main_crawler()