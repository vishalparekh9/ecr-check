import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
#Token
token = 'ABCGO'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobs.disneycareers.com/business/custom_fields.industrycustomfield/abc%20entertainment/391-28648/5' 

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
        self.domain = 'abc.go.com'
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
                # print(data)
                jobDataChunk = data.find('tbody')
                aTag = jobDataChunk.find_all('a')
                for link in aTag:
                    jobObj = deepcopy(self.obj)
                    token = link.get('href')
                    url = 'https://jobs.disneycareers.com' + str(token)
                    jobObj['url'] = url
                    isloaded, resJobData = self.get_request(url)
                    if isloaded:
                        jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                        if jobDetails:
                            jobObj['title'] = str(jobDetails.find('h1',{'id':'job-title-scrape'}).text.strip())
                            jobObj['location'] = str(jobDetails.find('span',{'class':'job-location-scrape'}).text.strip())
                            jobObj['description'] = jobDetails.find('div',{'class':'ats-description'})

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