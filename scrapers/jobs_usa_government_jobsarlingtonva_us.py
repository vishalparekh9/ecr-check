
import json

import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'JOBS_USA_GOVERNMENT_JOBSARLINGTONVA_US'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.governmentjobs.com/careers/arlington'

        self.getHeaders = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'ADRUM': 'isAjax:true',
            'Connection': 'keep-alive',
            'Content-Type': 'text/html',
            'Host': 'www.governmentjobs.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session = requests.session()
        self.domain = 'arlingtonva.us'
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

    def get_desc_request(self, url):
        try:
            descHeaders = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
            }
            res = self.session.get(url, headers=descHeaders)
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
                url = f'https://www.governmentjobs.com/careers/arlington?page={page}'
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    links = data.findAll("tr")
                    if len(links) > 1:
                        for link in links:
                            if link.find("h3") is not None:
                                jobObj = deepcopy(self.obj)
                                url = str("https://www.governmentjobs.com") + link.find("a").get("href")
                                jobObj['url'] = url
                                jobObj['title'] = link.find("a").text
                                jobObj['location'] = "United States"
                                isloaded, sres = self.get_desc_request(url)
                                if isloaded:
                                    try:
                                        jobDetails = BeautifulSoup(sres.text, "lxml")
                                        script = jobDetails.find("script", {"type": "application/ld+json"}).text
                                        jobDesc = json.loads(script)['description']
                                        jobObj['description'] = str(jobDesc)
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                            print(jobObj)
                                    except (Exception, AttributeError, KeyError, ValueError) as ex:
                                        pass
                    else:
                        isPage = False
                        break
                else:
                    print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))