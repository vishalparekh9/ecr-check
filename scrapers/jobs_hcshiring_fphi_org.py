
import json
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

# Token
token = 'JOBS_CATSONE_FPHI'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://fphi.org'

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
        self.domain = 'fphi.org'
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
            isPage = True
            while isPage:
                page = page + 1
                isloaded, res = self.get_request(f"https://fphi.hcshiring.com/49175da2/api/jobs?category=&distance=-1&filters=&internal=false&job=&jobSelected=false&location=&openOnly=false&orgId=&page={page}")
                if isloaded:
                    aTag = res.json()['jobs']
                    if aTag:
                        if len(aTag) > 0:
                            for link in aTag:
                                jobObj = deepcopy(self.obj)
                                jobId = link['id']
                                url = f"https://fphi.hcshiring.com/jobs/{jobId}"
                                jobObj['title'] = link['title']
                                jobObj['location'] = link['city'] + ", " + link['state']
                                jobObj['url'] = url
                                isloaded, jobres = self.get_request(f"https://fphi.hcshiring.com/49175da2/api/jobDescriptions?id={jobId}&preview=false&ref=&title=")
                                if isloaded:
                                    print("yes")
                                    jd = jobres.json()['jobDescriptions']['description']
                                    jobObj['description'] = str(jd)
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                        else:
                            break
                    else:
                        print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))