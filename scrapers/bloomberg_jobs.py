from pydoc import isdata
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'BLOOMBERG_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.bloomberg.com/job/search' 

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
        self.domain = 'bloomberg.com'
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
                isdata = True
                page = 0
                while isdata:
                    print("Collecting page: " + str(page))
                    url = 'https://careers.bloomberg.com/job_search/search_query?searchQueryString=nr%3D10000&_csrf=' + token
                    page = page + 40
                    isdata = False
                    isloaded, res = self.get_request(url, self.getajaxHeaders)
                    if 'jobData' not in res.json(): break
                    if len(res.json()['jobData']) == 0: break
                    links = res.json()['jobData']
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = 'https://careers.bloomberg.com/job/detail/' + str(link['JobReqNbr'])
                            jobObj['url'] = url
                            jobObj['title'] = link['JobTitle']
                            jobObj['location'] =link['Office']['City'] + ', ' + link['Office']['State']
                            jurl = 'https://careers.bloomberg.com/job_search/detail_query?jobID='+str(link['JobReqNbr'])+'&_csrf=' + token
                            isloaded, jobres = self.get_request(jurl, self.getajaxHeaders)
                            if isloaded:
                                jobObj['description'] = jobres.json()['jobDescription']
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