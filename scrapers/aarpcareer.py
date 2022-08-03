from random import betavariate
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
import json
from index import get_obj
#Token
token = 'AARP_CAREER'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.aarp.org/api/jobs?page=1&sortBy=relevance&descending=false&internal=false' 

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
        self.domain = 'careers.aarp.org'
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
            isdata = True
            page = 1
            while isdata:
                url = 'https://careers.aarp.org/api/jobs?page='+str(page)+'&sortBy=relevance&descending=false&internal=false'
                print("Collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    page = page + 1
                    if 'jobs' in res.json():
                        lis = res.json()['jobs']
                        if len(lis) == 0:
                            isdata=False
                            break
                        for link in lis:
                            a = link['data']['apply_url']
                            if a == None:
                                isdata = False
                                break
                            jobObj = deepcopy(self.obj)
                            url = 'https://careers.aarp.org/careers-home/jobs/' + str(link['data']['slug']) + '?lang=en-us'
                            jobObj['url'] = url
                            jobObj['location'] = link['data']['full_location']
                            jobObj['title'] = link['data']['title']
                            isloaded, jobres = self.get_request(url)
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            if isloaded:
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                descs = jobDetail.find('script',{'type':'application/ld+json'})
                                desc = json.loads(descs.text)
                                jobObj['description'] = desc['description']

                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        isdata = False
                        print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True
            isdata = False

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))