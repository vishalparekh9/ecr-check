import time
import random
import asyncio
from concurrent.futures import ProcessPoolExecutor
import functools

#custom files imports
import common as cf
import sitedirectory as scraper

if __name__ == "__main__":
    interval = random.uniform(0, 5)
    #time.sleep(interval)
    executor = ProcessPoolExecutor(5)
    loop = asyncio.get_event_loop()
    sites = cf.get_pending_sites()
    if sites:
        for site in sites:
            print(site)
            obj = scraper.SITEDIRECTORY(site).get_object()
            loop.run_in_executor(executor, functools.partial(cf.execute, obj, site))
            
            
