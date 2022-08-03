from pydoc import describe, isdata
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'HEALTHCARESOURCE_AULTMAN_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.company_token = 'aultman'
        self.baseUrl = 'https://pm.healthcaresource.com/CS/'+self.company_token+'/' 

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
            '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        }   
        self.session = requests.session()
        self.domain = 'aultcare.com'
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
    
    def post_request(self, page):
        try:
            url = 'https://pm.healthcaresource.com/JobseekerSearchAPI/'+self.company_token+'/api/Search'
            params = '{"query":{"bool":{"must":{"match_all":{}},"should":{"match":{"userArea.isFeaturedJob":{"query":true,"boost":1}}}}},"sort":{"title.raw":"asc"},"aggs":{"occupationalCategory":{"terms":{"field":"occupationalCategory.raw","size":1000}},"account":{"terms":{"field":"userArea.bELevel1DisplayName.raw","size":1000}},"employmentType":{"terms":{"field":"employmentType.raw","size":1000}}},"from":'+str(page)+',"size":25}'
            res = self.session.post(url, headers=self.postHeaders, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            page = 0
            isdata = True
            while isdata:
                isloaded, res = self.post_request(page)
                page = page + 25
                if isloaded:
                    if 'hits' not in res.json(): break
                    if 'hits' not in res.json()['hits']: break
                    if len(res.json()['hits']['hits']) == 0: break
                    jobList = res.json()['hits']['hits']
                    if jobList:
                        for job in jobList:
                            if '_source' not in job: continue
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = job['_source']['title']
                            id = str(job['_id']).split('_')[1]
                            url = 'https://pm.healthcaresource.com/CS/'+self.company_token+'/#/job/' + str(id)
                            jobObj['url'] = url
                            url ='https://pm.healthcaresource.com/JobseekerAPI/Site/'+self.company_token+'/api/v2/JobPostingV2?id=' + str(id)
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                try:
                                    jobObj['location'] = job['_source']['jobLocation']['address']['addressLocalityRegion']
                                except:
                                    pass
                                try:
                                    jobObj['description'] = jobres.json()['userArea']['jobSummaryDisplay']
                                except:
                                    pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['location'])
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