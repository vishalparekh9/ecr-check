
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os
import re
# Token
token = 'OPENTRONS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.opentrons.com/'

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
        self.domain = 'opentrons.com'
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
            url = 'https://opentrons.hrmdirect.com/employment/job-openings.php?search=true&nohd=&dept=-1&city=-1&state=-1&office=-1&cust_sort1=-1'
            isloaded, res = self.get_request(url)
            if isloaded:
                regex = re.compile('.*ReqRowClick ReqRowClick.*')
                data = BeautifulSoup(res.text, "lxml")
                links = data.find_all("tr", {"class": regex})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = str("https://opentrons.hrmdirect.com/employment/") + link.find("a").get("href")
                        jobObj['url'] = url
                        jobObj['title'] = link.find("a").text.replace("\r", "").replace("\n", "").strip()
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            jobDetails = BeautifulSoup(res.text, "lxml")
                            loc = jobDetails.find("table", {"class": "viewFields"}).find_all("tr")[2].text.replace("\r", "").replace("\n", "").replace("Location:", "").strip()
                            if len(loc) < 5:
                                jobObj['location'] = "United States / Remote"
                            else:
                                jobObj['location'] = loc
                            jobObj['description'] = str(jobDetails.find("div", {"class": "jobDesc"}))
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj['title'])
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))




