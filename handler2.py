import time
import random

import sitedirectory as scraper
import common as cf
from celery_runner import thread

if __name__ == "__main__":
    interval = random.uniform(0, 5)
    time.sleep(interval)
    sites = cf.get_pending_sites_internal_env()
    if len(sites) == 0:
        sites = cf.get_pending_sites_live()
    if sites:
        for site in sites:
            #obj = scraper.SITEDIRECTORY(site).get_object()
            thread.delay(site)
            time.sleep(0.5)
            print("message sent")
    else:
        print("no new sites found!")