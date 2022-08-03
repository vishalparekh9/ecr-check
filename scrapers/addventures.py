import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
#Token
token = 'ADDVENTURES'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://addventures.com/careers#block-position-listings-jobs' 

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
        self.domain = 'addventures.com'
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
                jobDataChunk = data.find('div',{'class':'views-element-container-inner'})
                if jobDataChunk:
                    aTag = jobDataChunk.find_all('a')
                    for link in aTag:
                        jobObj = deepcopy(self.obj)
                        url = link.get('href')
                        jobObj['url'] = url
                        isloaded, resJobData = self.get_request(url)
                        if isloaded:
                            jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                            
                            if jobDetails.text != '':
                                if 'add)' in str(jobDetails.find('div', {'class': 'banner'}).find('h1').text.split('(')):
                                    jobObj['title'] = "(" + str(jobDetails.find('div', {'class': 'banner'}).find('h1').text.split('(')[1]).strip()
                                else:
                                    jobObj['title'] = str(jobDetails.find('div', {'class': 'banner'}).find('h1').text.split('(')[0]).strip()
            
                                jobObj['location'] = str(jobDetails.find('div', {'class': 'banner'}).find('h1').text.split(')')[-2].split('(')[1]).strip()
            
                                jobObj['description'] = str(jobDetails.find('div',{'class','job_listing'})).strip()
                                
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