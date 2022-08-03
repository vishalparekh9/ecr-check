import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
import json
from index import get_obj
#Token
token = 'LABS1904'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://widgets.jobscore.com/jobs/1904labs/widget_iframe?' 

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
        self.domain = '1904labs.com'
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
                links = data.find_all('script',{'type':'text/javascript'})
                if links:
                    for link in links:
                        jsn = ''
                        if 'jobs_data_preload' in link.text:
                            try:
                                jsn = link.text.strip().split('};')[0]+'}'
                                jsn = jsn.split('jobs_data_preload')[1].strip().replace('= ','').strip()
                                jsn = json.loads(jsn)
                            except:
                                jsn = ''
                        else:
                            continue
                        if jsn == '':
                            continue
                        if 'jobs' in jsn:
                            for job in jsn['jobs']:
                                jobObj = deepcopy(self.obj)
                                jobObj['url'] = job['detail_url']
                                jobObj['title'] = job['title']
                                jobObj['location'] = job['location']
                                jobObj['description'] = job['description']
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