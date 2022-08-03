import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
#Token
token = '24G'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.24g.com/careers' 

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
        self.domain = '24g.com'
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
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                dataUrl = "https://app.jazz.co/widgets/basic/create/24g"
                isloaded, res = self.get_request(dataUrl)
                jobData = BeautifulSoup(res.text, 'lxml')
                if isloaded:
                    jobs = jobData.find('div',{'id':'resumator-jobs'})
                    allJobs = jobs.find_all('div',{'class':'resumator-job'})
                    for job in allJobs:
                        jobObj = deepcopy(self.obj)
                        jobObj['title'] = job.find('div',{'class':'resumator-job-title'}).text.strip()
                        jobObj['url'] = job.find('div',{'class':'resumator-job-title'}).text.strip()
                        jobObj['location'] = job.find('span',text='Location: ').next_sibling
                        
                        descs = job.find('div',{'class':'resumator-job-description'})
                        jobObj['description'] += str(descs)
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))