from random import betavariate
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
import json
from index import get_obj
#Token
token = '12THWONDER'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://12thwonder.kekahire.com/api/embedjobs/active/46d04007-cc44-4268-aac3-947fb7095d7a' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.getHeadersajax = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session = requests.session()
        self.domain = 'abbvie.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
    def get_request(self, url, headers):
        try:
            res = self.session.get(url, headers=headers)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl,self.getHeadersajax)
            if isloaded:
                if len(res.json()) > 0:
                    lis = res.json()
                    for link in lis:
                        a = link['id']
                        if a == None:
                            isdata = False
                            break
                        jobObj = deepcopy(self.obj)
                        url = 'https://12thwonder.kekahire.com/jobdetails/' + str(a)
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url,self.getHeaders)
                        jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                        if isloaded:
                            try:
                                jobObj['title'] = link['title']
                                jobObj['location'] = link['jobLocations'][0]['name'] + ', ' + link['jobLocations'][0]['state']
                                descs = jobDetail.find('div',{'class':'job-description-container'})
                                jobObj['description'] = str(descs)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                            except:
                                pass
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))