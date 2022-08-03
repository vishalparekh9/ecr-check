import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'DEERE_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobs.deere.com/search/?q=&sortColumn=referencedate&sortDirection=desc&searchby=location&d=5&startrow=0' 

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
        self.domain = 'warbyparker.com'
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
            page = 0
            isdata = True
            while isdata:
                url = 'https://jobs.deere.com/search/?q=&sortColumn=referencedate&sortDirection=desc&searchby=location&d=5&startrow='+str(page)
                print("Collecting rows from: " + str(page))
                page = page + 25
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('tr',{'class':'data-row clickable'})
                    if len(links) == 0: break
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = 'https://jobs.deere.com' + link.find('a',{'class':'jobTitle-link'}).get('href')
                        jobObj['url'] = url
                        jobObj['title'] = link.find('a',{'class':'jobTitle-link'}).text.strip()
                        jobObj['location'] = link.find('span',{'class':'jobLocation'}).text.strip()
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            jobObj['description'] = str(jobDetail.find('span',{'class':'jobdescription'}))
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))