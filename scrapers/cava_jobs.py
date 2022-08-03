from random import betavariate
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json
from index import get_obj

token = 'CAVA_JOBS'
class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://harri.com/support-center-hq'

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
            'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'x-csrf-token': 'undefined',
            'website-path': 'en',
            'env': 'undefined'
        }
        self.session = requests.session()
        self.domain = 'cava.com'
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
            token = None
            if isloaded:
                page = 0
                isdata = True
                self.postHeader['x-csrf-token'] = "null"
                while True:
                    url = 'https://gateway.harri.com/core/api/v1/harri_search/search_jobs'
                    params = '{"size":15,"source":"web","brand_level_ids":[801032],"postal_code_radius":"20","start":'+str(page)+',"sort":["publish_date"],"sort_type":"desc"}'
                    page = page + 15
                    isloaded, res1 = self.post_request(url, params)
                    if isloaded:
                        if 'data' not in res1.json(): break
                        if 'results' not in res1.json()['data']: break
                        if len(res1.json()['data']['results']) == 0: break
                        links = res1.json()['data']['results']
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = 'https://harri.com/cavatechnology/job/' + str(link['id']) + '-job'
                            jobObj['title'] = link['aliasPosition']
                            jobObj['location'] = link['locations'][0]['city'] + ', ' + link['locations'][0]['state']
                            url = 'https://gateway.harri.com/core/api/v2/profile/job/'+ str(link['id'])
                            isloaded, resdesc = self.get_request(url)
                            if 'job' in resdesc.json()['data']:
                                jobObj['description'] = resdesc.json()['data']['job']['description']
                            if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['description'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['title'])
        except Exception as e:
            print(e)
            self.iserror = True
            isdata = False

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))