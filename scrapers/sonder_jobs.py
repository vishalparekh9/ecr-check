import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import json
#Token
token = 'SONDER_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://boards-api.greenhouse.io/v1/boards/sonder/offices?render_as=tree' 

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
        self.domain = 'sonder.com'
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
                if 'offices' not in res.json(): return
                if len(res.json()['offices']) == 0: return
                for office in res.json()['offices']:
                    if 'departments' not in office: continue
                    if len(office['departments']) == 0: continue
                    for department in office['departments']:
                        if 'jobs' not in department: continue
                        if len(department['jobs']) == 0: continue
                        for job in department['jobs']:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = job['absolute_url']
                            url = 'https://boards-api.greenhouse.io/v1/boards/sonder/jobs/' + str(job['id'])
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                jobObj['title'] =jobres.json()['title']
                                jobObj['location'] = jobres.json()['location']['name']
                                jobObj['description'] = self.html_decode(jobres.json()['content'])
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))