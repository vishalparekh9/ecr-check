from random import betavariate
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json
from index import get_obj
import time
token = 'TCS_JOBS'
class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://ibegin.tcs.com/iBegin/jobs/search'

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
        }
        self.session = requests.session()
        self.domain = 'tcs.com'
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
            #time.sleep(0.5)
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
                page = 1
                while True:
                    url = 'https://ibegin.tcs.com/iBegin/api/v1/jobs/searchJ'
                    params = '{"jobCity":null,"jobSkill":null,"pageNumber":"'+str(page)+'","userText":"","jobTitleOrder":null,"jobCityOrder":null,"jobFunctionOrder":null,"jobExperienceOrder":null,"applyByOrder":null,"regular":true,"walkin":true}'
                    print("Collecting page: " + str(page))
                    page = page + 1
                    isloaded, res1 = self.post_request(url, params)
                    if isloaded:
                        if 'data' not in res1.json(): break
                        if 'jobs' not in res1.json()['data']: break
                        if len(res1.json()['data']['jobs']) == 0: break
                        links = res1.json()['data']['jobs']
                        print(links[0]['jobTitle'])
                            
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = 'https://ibegin.tcs.com/iBegin/jobs/' + str(link['id'])
                            jobObj['title'] = link['jobTitle']
                            jobObj['location'] = link['location']
                            try:
                                url = 'https://ibegin.tcs.com/iBegin/api/v1/job/desc?'
                                params = '{"jobId":"'+str(link['id']).replace(link['walkin'],'')+'"}'
                                self.postHeader['Referer'] = 'https://ibegin.tcs.com/iBegin/jobs/' + str(link['id'])
                                isloaded, resdesc = self.post_request(url, params)
                                if 'description' in resdesc.json()['data']:
                                    jobObj['description'] = resdesc.json()['data']['description']
                            except:
                                pass
                            if jobObj['description'] == '':
                                try:
                                    url = 'https://ibegin.tcs.com/iBegin/api/v1/job/desc/walkin'
                                    params = '{"jobId":"'+str(link['id']).replace(link['walkin'],'')+'"}'
                                    self.postHeader['Referer'] = 'https://ibegin.tcs.com/iBegin/jobs/' + str(link['id'])
                                    isloaded, resdesc = self.post_request(url, params)
                                    if 'qualifications' in resdesc.json()['data']:
                                        jobObj['description'] = resdesc.json()['data']['qualifications']
                                except:
                                    pass
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