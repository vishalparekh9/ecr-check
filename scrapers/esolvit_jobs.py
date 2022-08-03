from pydoc import isdata
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'ESOLVITE_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.esolvit.com/careers-opening?page=' 

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
        self.domain = 'esolvit.com'
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
            # regex = re.compile('.*job-desc-block.*')
            # descs = jobDetail.find_all('div',{'class':regex})
            page = 1
            isdata = True
            while isdata:
                surl = self.baseUrl + str(page)
                print("Collecting page: " + str(page))
                page = page + 1
                isloaded, res = self.get_request(surl)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('li',{'class':'pos-card'})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = 'https://www.esolvit.com/' + link.find('a').get('onclick').replace('jobredirect("','').replace('");','')
                            jobObj['url'] = url
                            jobObj['title'] = link.find('div',{'class':'title'}).text.strip()
                            jobObj['location'] = link.find('div',{'class':'date'}).text.strip()
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                jobObj['description'] = str(jobDetail.find('div',{'class':'col-sm-8 jobdesc'}))
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