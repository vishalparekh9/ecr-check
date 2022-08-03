import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
#Token
token = 'BIRDSMARKETING3'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.3birds.net/careers' 

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
        self.domain = '3birdsmarketing.com'
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
                # print(data.find('div',{'class':'twelve columns genContent'}))
                # jobDataChunk = data.find('div',{'class':'zpcontainer'})
                # aTag = jobDataChunk.find_all('a')
                # print(aTag)
                jobObj = deepcopy(self.obj)
                titles = []
                desc = []
                for jobTitles in data.find_all('div',{'class':'zpelement zpelem-heading'}):
                    if jobTitles.find('h4'):
                        titles.append(jobTitles.find('h4').text.strip())
                for jobDesc in data.find_all('div',{'class':'zpaccordion-icon-align-left'}):
                    if jobDesc:
                        desc.append(jobDesc)

                for (title,description) in zip(titles,desc):
                    jobObj['title'] = title
                    jobObj['description'] = description
                    jobObj['url'] = title
                    
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