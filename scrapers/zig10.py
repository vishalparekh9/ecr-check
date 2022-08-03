import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = '10ZIG'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.10zig.com/contact/career-opportunities' 

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
        self.domain = '10zig.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
    def get_request(self, url):
        try:
            res = self.session.get(url, headers=self.getHeaders)
            if res:
                return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                current_opportunities = data.find('div',{'class':'current-opportunities'})
                if current_opportunities:
                    jobArea = data.find_all('div',{'class':'job-area'})
                    if len(jobArea) > 0:
                        for jobdata in jobArea:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = jobdata.find('div',{'class':'job-title-area'}).text.replace('/','').replace('\t','').replace('\n','').replace('  ','').strip()
                            jobObj['title'] = jobdata.find('span',{'class':'job-title'}).text.strip()
                            jobObj['location'] = jobdata.find('span',{'class':'job-location'}).text.replace('/','').strip()
                            descs = jobdata.find('div',{'class':'job-description'})
                            jobObj['description'] += str(descs)
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