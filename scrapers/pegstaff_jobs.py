import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'PEGSTAFF_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www1.jobdiva.com/portal/?a=tijdnwy60icv5xk6mtb14jsauvwf8307dcwva6h0ev1r0dvgvcplcv6y521mad56#/' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.ajaxgetHeaders = {
            'a':'tijdnwy60icv5xk6mtb14jsauvwf8307dcwva6h0ev1r0dvgvcplcv6y521mad56',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            '*/*'
        }

        self.ajaxpostHeaders = {
            'a':'tijdnwy60icv5xk6mtb14jsauvwf8307dcwva6h0ev1r0dvgvcplcv6y521mad56',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'Host': 'ws.jobdiva.com',
            'Referer': 'https://www1.jobdiva.com/',
            'portalid': '2012'
        }
        self.session = requests.session()
        self.domain = 'pegstaff.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
    def get_request(self, url):
        try:
            res = self.session.get(url, headers=self.ajaxgetHeaders)
            return True, res
        except Exception as e:
            print(e)
        return False, False
    
    def post_request(self):
        try:
            url = 'https://ws.jobdiva.com/candPortal/rest/job/searchjobsportal'
            params = {
                "city": "",
                "country": "",
                "from": 1,
                "jobCategories": "",
                "jobDivisions": "",
                "jobTypes": "",
                "keywords": "",
                "miles": "",
                "onsiteFlex": "",
                "portalID": 1,
                "states": "",
                "to": 1500,
                "zipcode": "",
            }
            res = self.session.post(url, headers=self.ajaxpostHeaders, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            url = 'https://ws.jobdiva.com/candPortal/rest/auth/a'
            isloaded, res = self.get_request(url)
            if isloaded:
                token = res.json()['token']
                self.ajaxpostHeaders['token'] = token
                self.ajaxgetHeaders['token'] = token
                self.ajaxgetHeaders['portalid'] = "2012"
                isloaded, res = self.post_request()
                #isloaded, res = self.get_request(url)
                if 'data' not in res.json(): return 
                for link in res.json()['data']:
                    jobObj = deepcopy(self.obj)
                    jobObj['url'] = url
                    jobObj['title'] = link['title']
                    jobObj['location'] = link['location']
                    id = link['id']
                    url = 'https://www1.jobdiva.com/portal/?a=tijdnwy60icv5xk6mtb14jsauvwf8307dcwva6h0ev1r0dvgvcplcv6y521mad56#/jobs/' + str(id)
                    jobObj['url'] = url
                    isloaded, res1 = self.get_request('https://ws.jobdiva.com/candPortal/rest/job/getdetailbyjobid/'+str(id)+'?compid=')
                    if isloaded:
                        jobObj['description'] = res1.json()['job']['jobDescription']
                    if jobObj['title'] != '' and jobObj['url'] != '':
                        self.allJobs.append(jobObj)

        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))