import json
from pydoc import isdata
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re

from urllib3 import Retry
from index import get_obj
from urllib.parse import unquote
#Token
token = 'PERSISTENT_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.persistent.com/#!/' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.ajaxpostHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Accept':
            'application/json, text/plain, */*',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary0v8fAVhkfvjefMke',
        }
        self.session = requests.session()
        self.domain = 'persistent.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
    def get_request(self, url):
        try:
            res = self.session.get(url, headers=self.getHeaders, verify=False)
            return True, res
        except Exception as e:
            print(e)
        return False, False
    
    def post_request(self, page):
        try:
            url = 'https://careers.persistent.com/jobs/search'
            params = {
                'filterCri': '{"paginationStartNo":'+str(page)+',"selectedCall":"sort","sortCriteria":{"name":"modifiedDate","isAscending":false}}',
                'domain': 'careers.persistent.com'
            }
            res = self.session.post(url, headers=self.ajaxpostHeaders, data=params, verify=False)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                page = 0
                isdata = True
                while isdata:
                    print("collecting page:" + str(page))
                    isloaded, res = self.post_request(page)
                    print(res.text)
                    return
                    page = page + 9
                    if 'html' not in res.json(): break
                    html = res.json()['html']
                    data = BeautifulSoup(html, 'lxml')
                    regex = re.compile('.*link-with-arrow.*')
                    links = data.find_all('a',{'class':regex})
                    if len(links) == 0: break
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        jobObj['url'] = link.get('href')
                        isloaded, res1 = self.get_request("https://persistent.taleo.net/careersection/xxpsl_ex_cs/jobdetail.ftl?job=784949")
                        if isloaded:
                            try:
                                if 'api.fillList' in res1.text:
                                    jsn = res1.text.split('api.fillList(')[1]
                                    jsn = jsn.split(');')[0]
                                    jsn = jsn.split("'descRequisition',")[1]

                                soup = BeautifulSoup(unquote(jsn.split(",'")[11]), 'lxml')
                                jobObj['title'] = jsn.split("','")[9].replace("'","").strip()
                                if jobObj['location'] == '':
                                    jobObj['location'] = jsn.split("','")[17].replace("'","").strip()
                                if jobObj['location'] == '':
                                    jobObj['location'] = jsn.split("','")[16].replace("'","").strip()
                                
                                jobObj['description'] = unquote(jsn.split("','")[11]).replace('!*!','')
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