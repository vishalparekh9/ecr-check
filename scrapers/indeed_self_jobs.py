import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import os
import time
#Token
token = 'INDEED_SELF_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.indeed.com/cmp/Indeed/jobs' 

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
        self.domain = 'indeed.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
    def get_request(self, url):
        c = 0
        while True:
            try:
                res = self.session.get(url, headers=self.getHeaders, proxies={'http':'socks5://127.0.0.1:9050', 'https':'socks5://127.0.0.1:9050'})
                if 'hcaptcha solve page' not in res.text.lower(): 
                    return True, res
            except Exception as e:
                print(e)
            print("Checking try again:" + str(c))
            time.sleep(0.5)
            c = c + 1
            if c > 3: break
        return False, False
    
    def get_details(self, links):
        self.allJobs = []
        try:
            for link in links:
                time.sleep(1)
                jobObj = deepcopy(self.obj)
                #find a details
                url = 'https://www.indeed.com/viewjob?jk=' + link.get('data-tn-entityid').split(',')[1]
                jobObj['url'] = url
                jobObj['domain'] = "indeed.com"
                jobObj['company'] = "Indeed"
                found, resdetail = self.get_request(url)
                if found:
                    try:
                        soup = BeautifulSoup(resdetail.text, 'lxml')
                        jobObj['title'] = soup.find('h1').text
                        jobObj['location'] = link.find('div',{'data-testid':'jobListItem-location'}).text
                        try:
                            jobObj['location'] = jobObj['location'].replace(link.find('span',{'class':'more_loc_container'}).text,'')
                        except:
                            pass
                        regex = re.compile('.*jobsearch-JobComponent-description.*')
                        jobObj['description'] = str(soup.find('div',{'class':regex}))
                    except:
                        pass
                if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['location'] != '':
                    self.allJobs.append(jobObj)
        except:
            pass
    def process_logic(self):
        try:
            page = 0
            isdata = True
            while isdata:
                time.sleep(1)
                url = 'https://www.indeed.com/cmp/Indeed/jobs?start=' + str(page)
                page = page + 150
                print("collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    soup = BeautifulSoup(res.text, 'lxml')
                    regex = re.compile('.*job_.*')
                    links = soup.find_all('li',{'data-testid':'jobListItem'})
                    if len(links) == 0: break
                    next = soup.find('a',{'title':'Next'})
                    if not next: isdata = False
                    self.get_details(links)
                else:
                    isdata = False
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    obj = CRAWLER()
    obj.process_logic()