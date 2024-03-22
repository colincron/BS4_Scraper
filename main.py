import threading
from scraper import mainCrawler

if __name__ =="__main__":
    t1 = threading.Thread(target=mainCrawler)
    t2 = threading.Thread(target=mainCrawler)
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
 
    print("Done!")