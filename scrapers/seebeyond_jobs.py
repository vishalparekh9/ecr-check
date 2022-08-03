from random import betavariate
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json
from index import get_obj
token = 'SEEBEYOND_JOBS'
class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://oracle.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233'

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
            'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'tzname': 'Asia/Calcutta'
        }
        self.session = requests.session()
        self.domain = 'seebeyond.com'
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
    def post_request(self, url, page):
        try:
            params = '{"multilineEnabled":true,"sortingSelection":{"sortBySelectionParam":"3","ascendingSortingOrder":"false"},"fieldData":{"fields":{"KEYWORD":"","LOCATION":""},"valid":true},"filterSelectionParam":{"searchFilterSelections":[{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"JOB_TYPE","selectedValues":[]},{"id":"JOB_SCHEDULE","selectedValues":[]},{"id":"JOB_SHIFT","selectedValues":[]},{"id":"WILL_TRAVEL","selectedValues":[]},{"id":"POSTING_DATE","selectedValues":[]}]},"advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"ORGANIZATION","selectedValues":[]},{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"URGENT_JOB","selectedValues":[]},{"id":"WILL_TRAVEL","selectedValues":[]},{"id":"JOB_SHIFT","selectedValues":[]}]},"pageNo":'+str(page)+'}'
            res = self.session.post(url, headers=self.postHeader, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False
    
    def html_decode(self,s):
        """
        Returns the ASCII decoded version of the given HTML string. This does
        NOT remove normal HTML tags like <p>.
        """
        htmlCodes = (
                ("'", '&#39;'),
                ('"', '&quot;'),
                ('>', '&gt;'),
                ('<', '&lt;'),
                ('&', '&amp;'),
                (':','\:')
            )
        for code in htmlCodes:
            s = s.replace(code[1], code[0])
        return s

    
    def process_logic(self):
        try:
            isdata = True
            page = 1
            oldurl = ''
            while isdata:
                isloaded, res = self.post_request(self.baseUrl, page)
                page = page + 1
                print("collecting page: " + str(page))
                if not isloaded:
                    isdata = False
                    break
                if 'requisitionList' not in res.json(): break
                if len(res.json()['requisitionList']) == 0: break
                objs = res.json()['requisitionList']
                for obj in objs:
                    if 'column' not in obj:
                        if len(obj['column']) == 0:
                            continue
                    col = obj['column']
                    jobObj = deepcopy(self.obj)
                    url = 'https://oracle.taleo.net/careersection/2/jobdetail.ftl?job=' + col[2]
                    jobObj['url'] = url
                    jobObj['location'] = col[3].replace('["','').replace('"]','')
                    jobObj['title'] = col[0]
                    isloaded, res = self.get_request(url)
                    if isloaded:
                        jobDetail =  BeautifulSoup(res.text, 'lxml')
                        import urllib.parse
                        try:
                            jobObj['description'] = self.html_decode(urllib.parse.unquote(jobDetail.find('input',{'id':'initialHistory'}).get('value'))).split('!|!!*!')[1]
                            jobObj['description'] += self.html_decode(urllib.parse.unquote(jobDetail.find('input',{'id':'initialHistory'}).get('value'))).split('!|!!*!')[3]
                        except Exception as e:
                            pass
                        
                    if jobObj['title'] != '' and jobObj['url'] != '':
                        self.allJobs.append(jobObj)

        except Exception as e:
            print(e)
            self.iserror = True
            isdata = False

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))