
import json
from copy import deepcopy
import time
import requests
from bs4 import BeautifulSoup
from index import get_obj

token = 'JOBS_STATE_FARMS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.statefarm.com/'

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
        self.domain = 'statefarm.com'
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
                url = 'https://jobs.statefarm.com/api/jobs?page='+str(page)+'&sortBy=relevance&descending=false&internal=false&userId=61b1b667-a942-4312-83db-7e81aa4cf35e&sessionId=5674f2a6-c722-4093-846d-8e01f834afe2&deviceId=1036133625&domain=statefarm.jibeapply.com'
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
                            jobObj['description'] = str(link['data']['qualifications'] + "<br />" + link['data']['responsibilities'])
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

