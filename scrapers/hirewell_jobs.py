import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'HIREWELL_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://hirewell.com/jobs?combine=&location=&location-lat=&location-lng=&geolocation_geocoder_google_geocoding_api=&geolocation_geocoder_google_geocoding_api_state=1&page=' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.session = requests.session()
        self.domain = 'hirewell.com'
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
            page = 0
            isdata = True
            while isdata:
                print("collecting page: " + str(page))
                isloaded, res = self.get_request(self.baseUrl + str(page))
                page = page + 1
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('div',{'class':'job-card'})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = 'https://hirewell.com' + link.find('a').get('href')
                            jobObj['title'] = link.find('a').text.strip().replace('&nbsp;','')
                            jobObj['location'] = link.find('div',{'class':'location'}).text.strip()
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            if isloaded:
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                try:
                                    jobObj['description'] = str(jobDetail.find('div',{'class':'col-xs-12 col-sm-8 bs-region bs-region--left'}))
                                except:
                                    pass
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        isdata = False
                        print('No Job Data Found!')
                else:
                    isdata = False
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))