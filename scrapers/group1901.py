import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = '1901GROUP'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.leidos.com/search/jobs?q=%221901%22&ns_job_category=1901-jobs&page=' 

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
        self.domain = '1901group.com'
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
            page = 1
            isdata = True
            while isdata:
                url =self.baseUrl + str(page)
                print("collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                page = page + 1
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('div',{'class':'jobs-section__item space--small'})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = link.find('a').get('href')
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            if isloaded:
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                jobObj['title'] = link.find('a').text.strip()
                                jobObj['location'] = link.find('div',{'class':'large-3 columns'}).text.strip().replace('\n','').replace('\r','').replace('\t','').replace('  ','').replace('Location:','').strip()
                                jobObj['description'] = str(jobDetail.find('div',{'class':'job-details-description page-content'}))
                                
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        print('No Job Data Found!')
                        isdata = False
                else:
                    isdata = False
                                
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))