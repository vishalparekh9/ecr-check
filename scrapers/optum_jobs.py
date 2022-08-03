import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import json
#Token
token = 'OPTUM_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobsapi-google.m-cloud.io/api/job/search?callback=jobsCallback&pageSize=10&offset=20&companyName=companies%2F072a4277-f508-43f1-82a0-7cfb2b963d88&customAttributeFilter=ats_portalid%3D%22Smashfly%22&orderBy=posting_publish_time%20desc' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'accept: */*',
        }
        self.session = requests.session()
        self.domain = 'optum.com'
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
                url ='https://jobsapi-google.m-cloud.io/api/job/search?callback=jobsCallback&pageSize=100&offset='+str(page)+'&companyName=companies%2F072a4277-f508-43f1-82a0-7cfb2b963d88&customAttributeFilter=ats_portalid%3D%22Smashfly%22&orderBy=posting_publish_time%20desc'
                page = page + 100
                print("Collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                jsn = res.text.replace('jobsCallback(','').replace('})','}')
                jsn = json.loads(jsn)
                if isloaded:
                    if 'searchResults' not in jsn: break
                    if len(jsn['searchResults']) == 0: break                   
                    for jobs in jsn['searchResults']:
                        link = jobs['job']
                        jobObj = deepcopy(self.obj)
                        url1 = link['url']
                        jobObj['url'] = url1
                        jobObj['title'] = link['title']
                        jobObj['location'] = link['primary_city'] + ', ' + link['primary_state']
                        jobObj['description'] = link['description']
                        try:
                            for alt in link['addtnl_locations']:
                                jobObj['location'] += ' | ' + alt['addtnl_city'] + ', ' + alt['addtnl_state']
                        except:
                            pass
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))