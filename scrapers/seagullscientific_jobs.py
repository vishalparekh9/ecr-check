import re

import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'SEA_GULL_SCIENTIFIC_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.seagullscientific.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'referer': 'https://careers.trianz.com/SearchJobs/SearchJobs',
        }
        self.session = requests.session()
        self.domain = 'seagullscientific.com'
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
            url = 'https://seagullscientific.applytojob.com/apply/jobs/#'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                regex = re.compile('resumator_(.*?)_row')
                links = data.find("tbody").find_all("tr", {"class": regex})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = str("https://seagullscientific.applytojob.com" + link.find("a").get("href"))
                        if url is not None:
                            jobObj['url'] = url
                            jobObj['title'] = link.find("a").text.replace("\n", "").replace("\r", "").replace("Job Opening", "").strip()
                            jobObj['location'] = link.find_all('td')[1].text.replace("\n", "").replace("\r", "").strip()
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, 'lxml')
                                jobDesc = str(data.find('div', {'class': 'job_description'}))
                                if jobDesc:
                                    jobObj['description'] = jobDesc
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