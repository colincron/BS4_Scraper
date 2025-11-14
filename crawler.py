import sys
from functions import (timestamp, request_and_parse,
                       get_domain_names)

def main_crawler(start_url):
    url_list = [start_url,]
    i = 0

    while len(url_list) > 0:
        url = url_list[0]
        print("\n" + timestamp() + " Length of url_list: " + str(len(url_list)))
        print(timestamp() + " Number of sites crawled:" + str(i) + "\n")
        print(timestamp() + " Now searching: " + url)
        
        anchors = request_and_parse(url)
        url_list = get_domain_names(anchors,url_list)
        url_list.pop(0)
        i = i + 1
        
    else:
        sys.exit(timestamp() + " All done!")
