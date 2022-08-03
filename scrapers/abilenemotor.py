import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
#Token
token = 'ABILENEMOTOR'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.abilenemotor.com/jobs/' 

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
        self.domain = 'abilenemotor.com'
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
                for td in data.find_all('td',{'class':'job-name'}):
                    jobObj = deepcopy(self.obj)
                    url = td.find('a').get('href')
                    jobObj['url'] = url
                    isloaded, resJobData = self.get_request(url)
                    if isloaded:
                        jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                        jobObj['title'] = str(jobDetails.find('div',{'class':'job-info'}).find_previous('h2').text.strip())
                        jobObj['location'] = str(jobDetails.find('div',{'class':'job-location'}).text.strip())
                        jobObj['description'] = str(jobDetails.find('div',{'class':'job-content'}))
                            
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