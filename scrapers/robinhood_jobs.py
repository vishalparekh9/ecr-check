import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import json
#Token
token = 'ROBINHOOD_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://api.greenhouse.io/v1/boards/robinhood/jobs' 

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
        self.domain = 'robinhood.com'
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
    
    def html_decode(self,s):
        """
        Returns the ASCII decoded version of the given HTML string. This does
        NOT remove normal HTML tags like <p>.
        """
        htmlCodes = (
                ("'", '&#39;'),
                ('"', '&quot;'),
                ('>', '&gt;'),
                ('<', '&lt;'),
                ('&', '&amp;')
            )
        for code in htmlCodes:
            s = s.replace(code[1], code[0])
        return s

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                if 'jobs' not in res.json(): return
                if len(res.json()['jobs']) == 0: return
                for job in res.json()['jobs']:
                    jobObj = deepcopy(self.obj)
                    jobObj['url'] = job['absolute_url'].split('?')[0]
                    url = job['absolute_url'].split('?')[0]
                    isloaded, jobres = self.get_request(url)
                    if isloaded:
                        jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                        jobObj['title'] = jobDetail.find('h1').text.strip()
                        jobObj['location'] = jobDetail.find('div',{'class':'location'}).text.strip()
                        jobObj['description'] = str(jobDetail.find('div',{'id':'content'}))
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))