# jobs-json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'HUMANDOING'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'http://humansdoing.net/'

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
        self.domain = 'humansdoing.net'
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
            url = 'https://loxo.co/humans-doing'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find('script', {'id': 'jobs-json'}).text.replace("\r", "").replace("\n", "").strip()
                import json
                links = json.loads(links)
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = link['public_url']
                        title = link['public_title']
                        location = link['macro_address']
                        if location is None:
                            location = "United States"
                        jobObj['url'] = url
                        jobObj['title'] = title
                        jobObj['location'] = location
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            data = BeautifulSoup(res.text, 'lxml')
                            jobDesc = data.find("div", {"class": "public-job-description"})
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
    print(scraper.allJobs)



