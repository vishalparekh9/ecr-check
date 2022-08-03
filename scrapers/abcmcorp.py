import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
#Token
token = 'ABCMCORP'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.abcmcorp.com/employment/module/joblist/0?' 

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
        self.domain = 'abcmcorp.com'
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
                pagination = data.find('ul',{'class':'pagination'})
                pageList = []
                zerothLink = "<html><body><a href='https://www.abcmcorp.com/employment/module/joblist/0?'></a></body></html>"
                zerObj = BeautifulSoup(zerothLink,"lxml")
                pageList.append(zerObj.find('a'))
                pageList += pagination.find_all('a')[1:-2]
                for p in pageList:
                    pageUrl = p.get('href')
                    print(pageUrl)
                    if pageUrl != '#!':
                        isloaded, resJobData = self.get_request(pageUrl)
                        if isloaded:
                            jobList = BeautifulSoup(resJobData.text, 'lxml')
                            jobDataChunk = jobList.find('tbody',{'id':'jobAppyForm'})
                            if jobDataChunk:
                                aTag = jobDataChunk.find_all('a')
                                for link in aTag:
                                    jobObj = deepcopy(self.obj)
                                    url = link.get('href')
                                    if url != '#!':
                                        jobObj['url'] = url
                                        isloaded, resJobDetails = self.get_request(url)
                                        if isloaded:
                                            jobDetails = BeautifulSoup(resJobDetails.text, 'lxml')
                                            jobObj['title'] = str(jobDetails.find_all('table',{'class':'table table-bordered mb-4'})[1].find_all('td')[0].text.strip())
                                            jobObj['location'] =  str(jobDetails.find_all('table',{'class':'table table-bordered mb-4'})[0].find_all('td')[0].text.strip())
                                            jobObj['description'] =  str(jobDetails.find_all('div',{'class':'col-md-12 text-justify'})[1].text.strip())

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