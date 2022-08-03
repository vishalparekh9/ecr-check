import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
#Token
token = 'PAINTING360'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://360careers.careerplug.com/jobs#job_filters' 

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
        self.domain = '360painting.com'
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
                pages = ['https://360careers.careerplug.com/jobs#job_filters']
                pagination = data.find('div',{'class':'pagination'})

                if pagination:
                    aTag = pagination.find_all('a')
                    jobObj = deepcopy(self.obj)
                    for link in aTag[0:len(aTag)-1]:
                        token = link.get('href')
                        url = 'https://360careers.careerplug.com' + str(token)
                        pages.append(url)
                    for pageLink in pages:
                        isloaded, resJobData = self.get_request(pageLink)
                        if isloaded:
                            jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                            jobData = jobDetails.find('div',{'id':'job_table'})
                            aTag = jobData.find_all('a')
                            for link in aTag:
                                token = link.get('href')
                                jobUrl = 'https://360careers.careerplug.com' + str(token)
                                jobObj['url'] = jobUrl
                                isloaded, resJobDetails = self.get_request(jobUrl)
                                if isloaded:
                                    jobDetail = BeautifulSoup(resJobDetails.text, 'lxml')
                                    jobObj['title'] = str(jobDetail.find('h1',{'class':'headline'}).text.strip())
                                    jobObj['description'] = str(jobDetail.find('div',{'class':'job-description-container'}).text.strip())

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