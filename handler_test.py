#from crawler_test import thread
#commented on 21-06-2022
from celery_runner import thread
import time
import random

import sitedirectory as scraper
import common as cf

if __name__ == "__main__":
    #interval = random.uniform(0, 5)
    #time.sleep(interval)
    sites = cf.get_pending_sites_test_env()
    if sites:
        for site in sites:
            #obj = scraper.SITEDIRECTORY(site).get_object()
            thread.delay(site)
            time.sleep(0.5)
            print("message sent")
    else:
        print("no new sites found!")