import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json

from urllib3 import Retry
from index import get_obj

token = 'FREEMO_JOBS'
class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.builtinseattle.com/company/freemo/jobs'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.postHeader = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Accept':
            '*/*',
            'Content-Type': 'application/json',
        }
        self.session = requests.session()
        self.domain = 'getfreemo.com'
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
        
    def post_request(self, url, params):
        try:
            #params = '{"limit":20,"offset":'+str(page)+',"appliedFacets":{},"searchText":""}'
            res = self.session.post(url, headers=self.postHeader, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    
    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                url = 'https://api.builtin.com/graphql'
                params = '{"operationName":"GetSimilarCompaniesAndJobs","variables":{"id":7533,"categoryId":-1},"query":"query GetSimilarCompaniesAndJobs($id: Int!, $categoryId: Int!) {  companyByID(id: $id) {    id    similarCompaniesAndJobs(categoryID: $categoryId) {      id      name      alias      logo      featuredImage      isBrandBoost      jobs {        count      }      industries {        name      }      city      state      url      marketSites {        regionID      }      subscription {        level      }      jobDetails(categoryID: $categoryId) {        id        title        categoryID        location        originalLocation        url        remoteStatus        company {          id          logo          name        }      }    }  }}"}'
                isloaded, res1 = self.post_request(url, params)
                if isloaded:
                    if 'data' not in res1.json(): return
                    if 'companyByID' not in res1.json()['data']: return
                    if 'similarCompaniesAndJobs' not in res1.json()['data']['companyByID']: return
                    links = res1.json()['data']['companyByID']['similarCompaniesAndJobs']
                    for link in links:
                        for job in link['jobDetails']:
                            jobObj = deepcopy(self.obj)
                            url = job['url']
                            jobObj['url'] = job['url']
                            jobObj['title'] = job['title']
                            jobObj['location'] = job['originalLocation']
                            isloaded, resdesc = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(resdesc.text, 'lxml')
                                jobObj['description'] = str(data.find('div',{'class':'node__content'}))
                            if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['description'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['title'])
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))