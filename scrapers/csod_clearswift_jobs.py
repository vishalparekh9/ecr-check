import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import json
token = 'CSOD_CLEARSWIFT_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.myhost = 'helpsystems^1'
        self.baseUrl = 'https://'+self.myhost.split('^')[0]+'.csod.com/ux/ats/careersite/'+self.myhost.split('^')[1]+'/home?c='+self.myhost.split('^')[0]
        self.cloud = ''
        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.postHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'application/json; q=1.0, text/*; q=0.8, */*; q=0.1',
            'authorization': '',
            'content-type': 'application/json',
            'referer': 'https://'+self.myhost.split('^')[0]+'.csod.com/'
        }
        self.session = requests.session()
        self.domain = 'clearswift.com'
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
    
    def post_request(self, params):
        try:
            res = self.session.post( self.cloud + 'rec-job-search/external/jobs', headers=self.postHeaders, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                token = ''
                data = BeautifulSoup(res.text, 'lxml')
                for script in data.find_all('script'):
                    if '"token"' in str(script):
                        token = str(script).split('csod.context=')[1].split('};')[0] + '}'
                        self.cloud = json.loads(token)['endpoints']['cloud']
                        token = json.loads(token)['token']
                isdata = True
                page = 1
                while isdata:
                    self.postHeaders['authorization'] = 'Bearer ' + token
                    self.getHeaders['authorization'] = 'Bearer ' + token
                    params = '{"careerSiteId":'+self.myhost.split('^')[1]+',"careerSitePageId":'+self.myhost.split('^')[1]+',"pageNumber":'+str(page)+',"pageSize":25,"cultureId":1,"searchText":"","cultureName":"en-US","states":[],"countryCodes":[],"cities":[],"placeID":"","radius":null,"postingsWithinDays":null,"customFieldCheckboxKeys":[],"customFieldDropdowns":[],"customFieldRadios":[]}'
                    print("Collecting page " + str(page))
                    page = page + 1
                    isloaded, res = self.post_request(params)
                    if 'data' not in res.json(): break
                    if len(res.json()['data']) == 0: break
                    if 'requisitions' not in res.json()['data']: break
                    if len(res.json()['data']['requisitions']) == 0: break
                    links = res.json()['data']['requisitions']
                    for link in links:
                        url = 'https://'+self.myhost.split('^')[0]+'.csod.com/ux/ats/careersite/1/home/requisition/' + str(link['requisitionId'])+'?c='+self.myhost.split('^')[0]
                        jobObj = deepcopy(self.obj)
                        jobObj['url'] = url
                        jobObj['title'] = link['displayJobTitle']
                        if 'locations' in link:
                            for loc in link['locations']:
                                try:
                                    if jobObj['location'] == "":
                                        jobObj['location'] = loc['city'] + ', ' + loc['state']
                                    else:
                                        jobObj['location'] += ' | ' + loc['city'] + ', ' + loc['state']
                                except:
                                    jobObj['location'] = 'United States'
                        url = 'https://'+self.myhost.split('^')[0]+'.csod.com/Services/API/ATS/CareerSite/1/JobRequisitions/'+ str(link['requisitionId'])+'?useMobileAd=false&cultureId=1'
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            try:
                                jobObj['description'] = jobres.json()['data'][0]['items'][0]['fields']['ad']
                            except Exception as e:
                                print(e)
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