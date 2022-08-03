
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'ROBERTHALF_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.roberthalf.com'

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
        self.domain = 'roberthalf.com'
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
                url = 'https://www.roberthalf.com/ajax/job-results?page='+str(page)+''
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = res.json()['jobs']
                    if len(data) > 0:
                        for link in data:
                            jobObj = deepcopy(self.obj)
                            url = str("https://www.roberthalf.com"+str(link['url'])+"/")
                            jobObj['url'] = url
                            jobObj['title'] = link['title']
                            jobObj['location'] = link['location']
                            jobObj['description'] = str(link['description'] + " <br /> " + link['requirements'])
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                    else:
                        print("Job Not Found!")
                        ispage = False
                        break

            else:
                print("Job Not Found!")
                ispage=False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)