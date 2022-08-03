import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import json
#Token
token = 'DRIP_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.drip.com/careers' 

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
        self.domain = 'drip.com'
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
            # regex = re.compile('.*job-listings_.*')
            # descs = jobDetail.find_all('div',{'class':regex})
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                soup = BeautifulSoup(res.text, 'lxml')
                #regex = re.compile('.*job-listings_.*')
                links = soup.find_all('a',{'class':'job-listing'})
                for link in links:
                    jobObj = deepcopy(self.obj)
                    try:
                        jobObj['title'] = link.find('div',{'class':'job-listing__role'}).text.strip()
                        jobObj['location'] = link.find('div',{'class':'job-listing__location'}).text.strip()
                        jobObj['url'] = 'https://www.drip.com' + link.get('href')
                        isloaded, res1 = self.get_request(jobObj['url'])
                        if isloaded:
                            soup1 = BeautifulSoup(res1.text, 'lxml')
                            jobObj['description'] = str(soup1.find('section',{'class':'page-section page-section--md page-section--collapse-top'}))
                    except:
                        pass
                    if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['description'] != '':
                        self.allJobs.append(jobObj)
                        print(jobObj['title'])
                        print(jobObj['location'])
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))