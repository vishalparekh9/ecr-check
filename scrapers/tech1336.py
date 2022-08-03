from random import betavariate
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
import json
from index import get_obj
#Token
token = 'ABBVIECAREER'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://cubicpv.com/careers/#current-openings' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
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
            isloaded, res = self.get_request(self.baseUrl,self.getHeaders)
            if isloaded:
                soup = BeautifulSoup(res.text, 'lxml')
                alinks = soup.find_all('h3',{'class':'elementor-post__title'})
                if alinks:
                    for link in alinks:
                        a = link.find('a')
                        if a == None:
                            continue
                        jobObj = deepcopy(self.obj)
                        url = a.get('href')
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url,self.getHeaders)
                        jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                        if isloaded:
                            try:
                                jobObj['title'] = jobDetail.find('h1').text.strip()
                                jobObj['location'] = ''
                                descs = jobDetail.find('div',{'class':'jupiterx-post-body'})
                                jobObj['description'] = str(descs).split('noscript ')[0]
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                print(jobObj)
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