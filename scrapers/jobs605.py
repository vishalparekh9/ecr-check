import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
#Token
token = '605_TV'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.605.tv/company/careers/' 

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
        self.domain = '605.tv'
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
                jobDataChunk = data.find('div',{'class':'jss162 jss161 jobposts'})
                if jobDataChunk:
                    aTag = jobDataChunk.find_all('a')
                    for link in aTag:
                        jobObj = deepcopy(self.obj)
                        token = link.get('href').split('/')[5]
                        url = 'https://apply.workable.com/api/v2/accounts/605/jobs/' + str(token)
                        jobObj['url'] = 'https://apply.workable.com/605/j/' + str(token)
                        isloaded, resJobData = self.get_request(url)
                        if isloaded:
                            if resJobData.text != 'Job not found':
                                jobDetail = json.loads(resJobData.text)
                                jobObj['title'] = jobDetail['title']
                                
                                jobObj['location'] = jobDetail['location']['city']
                                
                                jobObj['description'] = jobDetail['description']

                                if 'requirements' in jobDetail:
                                    jobObj['description'] += jobDetail['requirements']
                                
                                if 'benefits' in jobDetail:
                                    jobObj['description'] += jobDetail['benefits']
                                
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