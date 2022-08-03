

import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
import json

from index import get_obj

token = 'AMERICASHLOANS'

id = 'f627c084-1326-4737-b657-420dd279b78f'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://recruiting.paylocity.com/Recruiting/Jobs/All/'+str(id) + '' 

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
        self.domain = 'americashloans.net'
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
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('script')
                if links:
                    for link in links:
                        jsn = ''
                        try:
                            if 'window.pageData' in link.text:
                                jsn = link.text.strip().split('};')[0]+'}'
                                jsn = jsn.split('window.pageData')[1].strip().replace('= ','').strip()
                                jsn = json.loads(jsn)
                        except:
                            pass
                        if jsn == '':
                            continue
                        if 'Jobs' in jsn:
                            data = jsn['Jobs']
                            for job in jsn['Jobs']:
                                url ='https://recruiting.paylocity.com/Recruiting/Jobs/Details/' + str(job['JobId'])
                                jobObj = deepcopy(self.obj)
                                jobObj['url'] = url
                                isloaded, jobres = self.get_request(url)
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                if isloaded:
                                    jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                    jobObj['title'] = jobDetail.find('span',{'class':'job-preview-title left'}).text.strip()
                                    jobObj['location'] = jobDetail.find('div',{'class':'preview-location'}).text.strip()
                                    jobObj['description'] = str(jobDetail.find('div',{'class':'job-preview-details'}))
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    
                