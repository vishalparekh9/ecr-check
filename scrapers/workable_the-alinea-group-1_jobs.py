import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json
from index import get_obj

token = 'WORKABLE_THE-ALINEA-GROUP-1_JOBS'
class CRAWLER(object):
    def __init__(self):
        self.site_name = 'the-alinea-group-1'
        self.baseUrl = 'https://apply.workable.com/'+self.site_name+'/'

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
        self.domain = 'alinearestaurant.com'
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
            token = ''
            if isloaded:
                isdata = True
                self.postHeader['x-csrf-token'] = token
                while True:
                    print("collecting token: " + token)
                    url = 'https://apply.workable.com/api/v3/accounts/'+self.site_name+'/jobs'
                    params = '{"token":"'+str(token)+'","query":"","location":[],"department":[],"worktype":[],"remote":[]}'
                    isloaded, res1 = self.post_request(url, params)
                    if isloaded:
                        if 'results' not in res1.json(): break
                        if len(res1.json()['results']) == 0: break
                        links = res1.json()['results']
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = 'https://apply.workable.com/'+self.site_name+'/j/' + str(link['shortcode']) + '/'
                            jobObj['title'] = link['title']
                            jobObj['location'] = link['location']['city'] +', ' + link['location']['region']
                            url = 'https://apply.workable.com/api/v2/accounts/'+self.site_name+'/jobs/' + str(link['shortcode'])
                            isloaded, resdesc = self.get_request(url)
                            if 'description' in resdesc.json():
                                jobObj['description'] = resdesc.json()['description']
                                jobObj['description'] = jobObj['description'] + '<br>' + resdesc.json()['requirements']
                                jobObj['description'] = jobObj['description'] + '<br>' + resdesc.json()['benefits']
                            if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['description'] != '':
                                self.allJobs.append(jobObj)
                        if 'nextPage' not in  res1.json(): break
                        token = res1.json()['nextPage']
        except Exception as e:
            print(e)
            self.iserror = True
            isdata = False

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))