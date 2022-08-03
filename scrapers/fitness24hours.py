import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = '24HOURFITNESS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.24hourfitness.com/club-careers/new-jobs/ajax/joblisting/?num_items=15&offset=0' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.session = requests.session()
        self.domain = '24hourfitness.com'
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
                url = 'https://careers.24hourfitness.com/club-careers/new-jobs/ajax/joblisting/?num_items=15&offset='+str(page) 
                page = page + 15
                print("Collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('li',{'class':'direct_joblisting with_description'})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url =  'https://careers.24hourfitness.com' + link.find('a').get('href')
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            if isloaded:
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                jobObj['title'] = link.find('a').text.strip().replace('\n','').replace('\r','').replace('  ','')
                                jobObj['location'] = link.find('div',{'class':'direct_joblocation'}).text.strip().replace('\n','')
                                jobObj['description'] = str(jobDetail.find('div',{'id':'direct_jobDescriptionText'}))
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        isdata = False
                        print('No Job Data Found!')
                else:
                    isdata = False
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))