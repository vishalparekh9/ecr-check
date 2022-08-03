import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import json
#Token
token = 'TRUPLAY_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://app.crelate.com/api/candidateportal/GetAllJobs?requestEnvelope=%7B%22Locations%22%3Anull%2C%22OrganizationId%22%3A%22acd43ae0-69b2-417f-ea98-6de5e6e4d808%22%2C%22SearchText%22%3Anull%2C%22Tags%22%3Anull%7D' 

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
        self.domain = 'truplaygames.com'
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
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                if 'Jobs' not in res.json(): return
                if len(res.json()['Jobs']) == 0: return
                links = res.json()['Jobs']
                for link in links:
                    jobObj = deepcopy(self.obj)
                    try:
                        jobObj['title'] = link['Title']
                        jobObj['location'] = link['City'] + ', ' + link['State']
                        jobObj['url'] = 'https://app.crelate.com/portal/truplaygames/job' + link['Url']
                        url = 'https://app.crelate.com/api/candidateportal/GetJob?requestEnvelope=%7B%22JobCode%22%3A%22'+str(link['Url'].replace('/',''))+'%22%7D'
                        isloaded, res1 = self.get_request(url)
                        if isloaded and 'Job' in res1.json():
                            jobObj['description'] = res1.json()['Job']['Description']                        
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