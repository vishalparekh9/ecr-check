
import json
from copy import deepcopy
import time
import requests
from bs4 import BeautifulSoup
from index import get_obj

token = 'CAREERS_SERVICE_NOW_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.servicenow.com/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.session = requests.session()
        self.domain = 'servicenow.com'
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
            ispage = True
            while ispage:
                page = page + 1
                print(page)
                url = 'https://careers.servicenow.com/api/jobs?page='+str(page)+'&sortBy=relevance&descending=false&internal=false&tags8=OFFER%7CSOURCING%7CINTERVIEW'
                isloaded, res = self.get_request(url)
                if isloaded:
                    links = res.json()['jobs']
                    totalHints = res.json()["totalCount"]
                    if page > totalHints:
                        break
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = str(link['data']['title'])
                            jobObj['location'] = str(link['data']['full_location'])
                            jobObj['description'] = str(link['data']['description'])
                            jobObj['url'] = str(link['data']['apply_url'])
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                    else:
                        isdata = False
                        break
            else:
                isdata = False
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))

