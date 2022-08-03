import re

import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'LBL_REFERALS_SELECTMINDS_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.lbl.gov'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'lbl.gov'
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
            page = 0
            isPage = True
            while isPage:
                page = page + 1
                print("Collecting for page ", page)
                url = f'https://lbl.referrals.selectminds.com/jobs/search/2932287/page{page}'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(str(res.text), "lxml")
                    links = data.find_all("div", {"class": "jlr_title"})
                    if len(links) > 0:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = link.find("p", {"class": "jlr_company"}).text.replace("\r", "").replace("\n", "").replace("\t", "").strip()
                            url = str("" + link.find("a").get("href"))
                            jobObj['url'] = url
                            jobObj['location'] = link.find("span", {"class": "location"}).text.replace("\r", "").replace("\n", "").replace("\t", "").strip()
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                jobData = BeautifulSoup(res.text, "lxml")
                                jobDesc = jobData.find("div", {"class": "job_description"})
                                jobObj['description'] = str(jobDesc)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        isPage = False

            else:
                print("Job Not Found")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)
