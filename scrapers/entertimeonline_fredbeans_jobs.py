import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
import re
#Token
token = 'ENTERTIMEONLINE_FREDBEANS_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.careerurl = 'https://secure4.entertimeonline.com^6120773'
        self.host = self.careerurl.split('^')[0]
        self.company = self.careerurl.split('^')[1]

        self.baseUrl = self.host + '/ta/rest/ui/recruitment/companies/%7C'+self.company+'/job-requisitions?offset=' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'Accept':
            'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.session = requests.session()
        self.domain = 'fredbeans.com'
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
                print("collecting page " + str(page))
                isloaded, res = self.get_request(self.baseUrl + str(page))
                #print(self.baseUrl + str(page))
                page = page + 100
                if isloaded:
                    if 'job_requisitions' not in res.json(): break
                    if len(res.json()['job_requisitions']) == 0: break
                    links = res.json()['job_requisitions']
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = self.host + '/ta/' + str(self.company) + '.careers?ApplyToJob=' + str(link['id'])
                            jobObj['url'] = url
                            jobObj['title'] = link['job_title']
                            try:
                                jobObj['location'] = link['location']['city'] + ', ' + link['location']['state']
                            except:
                                pass
                            url = self.host + '/ta/rest/ui/recruitment/companies/%7C'+(self.company)+'/job-requisitions/' + str(link['id'])
                            isloaded, resJobData = self.get_request(url)
                            if isloaded:
                                try:
                                    jobObj['description'] = resJobData.json()['job_description'] + ' <br> <b>job requirement</b> <br>' + resJobData.json()['job_requirement']
                                    jobObj['description'] = jobObj['description'] + ' <br>' + resJobData.json()['job_preview']
                                except:
                                    pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['title'])
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