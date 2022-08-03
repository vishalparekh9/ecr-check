from random import betavariate
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'DEVCOLOR_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobs.devcolor.org/jobs/search?criteria=&location=' 

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
        self.domain = 'devcolor.org'
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
            isdata = True
            page = 1
            while isdata:
                url = 'https://jobs.devcolor.org/jobs/search?criteria=&location=&page='+str(page)
                print("Collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    page = page + 1
                    data = BeautifulSoup(res.text, 'lxml')
                    if data:
                        regex = re.compile('.*list-group-item job-search-result clickable.*')
                        lis = data.find_all('div',{'class':regex})
                        if len(lis) == 0:
                            isdata = False
                            break
                        for link in lis:
                            a = link.find('a')
                            if a == None:
                                isdata = False
                                break
                            jobObj = deepcopy(self.obj)
                            url = 'https://jobs.devcolor.org' + a.get('href')
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            if isloaded:
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                jobObj['title'] = jobDetail.find('h1').text.strip()
                                
                                jobObj['location'] = jobDetail.find('span',{'class','block-job-location'}).text.strip().strip()
                                
                                regex = re.compile('.*iCIMS_InfoMsg.*')
                                descs = jobDetail.find('div',{'class':'col-md-8 width-xxs-100'})
                                jobObj['description'] = str(descs)
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