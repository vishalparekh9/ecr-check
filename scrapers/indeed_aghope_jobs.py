import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'INDEED_AGHOPE_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.indeed.com/cmp/A-Greater-Hope-1/jobs' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.postHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'indeed-api-Key': '80caa2d5585ed6f127d0fd62c5451a565f8777048e67a4877f00c5640df37f3f'
        }
        self.session = requests.session()
        self.domain = 'aghope.org'
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
    
    def post_request(self, keyid):
        try:
            url = 'https://apis.indeed.com/graphql?co=US'
            data = '{"query":"    query CompJobsPageFetchJobData($jobKey: ID!) {        jobData(jobKeys: [$jobKey]) {            results {                job {                    key                    title                    description {                        html                    }                    indeedApply {                        scopes                    }                    location {                        countryCode                    }                }            }        }    }","variables":{"jobKey":"'+str(keyid)+'"}}'
            res = self.session.post(url, headers=self.postHeaders, data=data)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            page = 0
            isdata = True
            oldkey = []
            while isdata:
                url = self.baseUrl + '?start=' + str(page)
                print("collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                page = page + 150
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    divs = data.find('ul',{'data-testid':'jobList'})
                    if divs == None: break
                    divs = divs.find_all('li')
                    if divs[0].get('data-tn-entityid').split(',')[1] in oldkey: break
                    oldkey.append(divs[0].get('data-tn-entityid').split(',')[1].strip())
                    for div in divs:
                        keyid = div.get('data-tn-entityid').split(',')[1]
                        isloaded, res = self.post_request(keyid)
                        if isloaded and 'data' in res.json():
                            if len(res.json()['data']['jobData']['results']) == 0:
                                continue
                            for link in res.json()['data']['jobData']['results']:
                                jobObj = deepcopy(self.obj)
                                url =  self.baseUrl + '?jk='+ str(keyid) + '&start=0'
                                jobObj['url'] = url
                                jobObj['title'] = link['job']['title']
                                jobObj['location'] = div.find('div',{'data-testid':'jobListItem-location'}).text.strip()
                                jobObj['description'] = link['job']['description']['html']
                                
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                        else:
                            print('No Job Data Found!')
                            isdata = False
                        
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))