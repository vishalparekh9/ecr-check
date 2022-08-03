import re

import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'ONE_CLICK_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://oneclick.ai/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'oneclick.ai'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def get_request(self, url):
        try:
            res = self.session.get(url, headers=self.getHeaders)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            url = f'https://www.oneclick.ai/en/careers'
            print(url)
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                fs = re.compile("overflow element(.*?)home")
                links = data.find_all("div", {"class": fs})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = str("https://www.oneclick.ai") + link.find("a").get("href")
                        jobObj['url'] = url
                        jobObj['title'] = link.find("h4").text.replace("                    ", " - ").replace("\r", "").replace("\n", "").strip()
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            jobDetails = BeautifulSoup(res.text, "lxml")
                            jobObj['location'] = str("United States")

                            jobObj['description'] = str(jobDetails.find("div", {"class": "col-md-9 aligncenter"}))
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))