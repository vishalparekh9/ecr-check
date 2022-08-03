from pydoc import isdata
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import json
#Token
token = 'CSLBEHRING_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://csl.recsolu.com/job_boards/rAD_La6OkYhQxVTHz3rLgA' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }

        self.getajaxHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            '*/*',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.session = requests.session()
        self.domain = 'cslbehring.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
        
    def get_request(self, url, header):
        try:
            res = self.session.get(url, headers=header)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            # regex = re.compile('.*job-desc-block.*')
            # descs = jobDetail.find_all('div',{'class':regex})
            isloaded, res = self.get_request(self.baseUrl, self.getHeaders)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                token = data.find('meta',{'name':'csrf-token'}).get('content')
                for script in data.find_all('script'):
                    if 'xpid' in str(script):
                        xpid = str(script).split('xpid')[1]
                        xpid = xpid.split('"')[1]
                self.getajaxHeaders['x-csrf-token'] = token
                self.getajaxHeaders['x-newrelic-id'] = xpid
                isdata = True
                page = 1
                while isdata:
                    print("Collecting page: " + str(page))
                    url = 'https://csl.recsolu.com/job_boards/rAD_La6OkYhQxVTHz3rLgA/search?query=&filters=1418,6893,6887&job_board_tab_identifier=af546986-e703-2eb9-c416-2472040ea84c&page_number='+str(page)+''
                    page = page + 1
                    isloaded, res = self.get_request(url, self.getajaxHeaders)
                    if 'html' not in res.json(): break
                    data = BeautifulSoup(res.json()['html'], 'lxml')
                    links = data.find_all('li')
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = 'https://csl.recsolu.com' + link.find('a',{'class':'search-results__req_title'}).get('href').split('?')[0]
                            jobObj['url'] = url
                            jobObj['title'] = link.find('a',{'class':'search-results__req_title'}).text
                            for span in link.find_all('span')[::-1]:
                                jobObj['location'] += span.text + ", "
                            isloaded, jobres = self.get_request(url, self.getHeaders)
                            if isloaded:
                                data1 = BeautifulSoup(jobres.text, 'lxml')
                                jobObj['description'] = str(data1.find('section',{'class':'job-details__description pull-left'}))
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['title'])
                    else:
                        isdata = False
                        print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))