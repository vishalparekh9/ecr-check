
import re

import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOBS_SELECTMINDS_COM_VERSITI'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://versiti.referrals.selectminds.com/'

        self.getHeaders = {
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
          'Connection': 'keep-alive',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
          'X-Requested-With': 'XMLHttpRequest'
        }

        self.session = requests.session()
        self.domain = 'versiti.org'
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
            url = f'https://versiti.referrals.selectminds.com/'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find_all("div", {"class": "jlr_right_hldr"})
                if len(links) > 0:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        jobObj['title'] = link.find("a").text
                        url = link.find("a").get("href")
                        jobObj['url'] = url
                        jobObj['location'] = link.find("a", {"class": "location"}).text
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            jobData = BeautifulSoup(res.text, "lxml")
                            jobDesc = jobData.find("div", {"class": "job details"})
                            jobObj['description'] = str(jobDesc)
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                else:
                    print("Job Not Found")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))