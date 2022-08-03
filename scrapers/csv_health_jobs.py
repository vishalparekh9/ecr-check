
import json
from copy import deepcopy
import time
import requests
from bs4 import BeautifulSoup
from index import get_obj

token = 'CVS_HEALTH_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.cvs.com'

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
        self.domain = 'cvs.com'
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
            page = -101
            ispage = True
            while ispage:
                page = page + 101
                print(page)
                url = 'https://jobsapi-google.m-cloud.io/api/job/search?pageSize=100&offset='+str(page)+'&companyName=companies%2F39e30343-8bbb-42cd-8e86-6734943cb4b9&orderBy=posting_publish_time%20desc'
                isloaded, res = self.get_request(url)
                if isloaded:
                    links = res.json()['searchResults']
                    totalHints = res.json()["totalHits"]
                    if page > totalHints:
                        break
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = str(link['job']['title'])
                            jobObj['location'] = str(link['job']['primary_city'] + str(" - ") + link['job']['primary_state'])
                            jobObj['description'] = str(link['job']['description'])
                            jobObj['url'] = 'https://jobs.cvshealth.com/job/' + str(link['job']['id']) + '/job/'
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['url'])
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

