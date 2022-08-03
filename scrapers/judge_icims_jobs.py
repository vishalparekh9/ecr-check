import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

# Token
token = 'CAREERS_JUDGE_JOBS_ICIMS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers-judge.icims.com/jobs/search?ss=1&hashed=-625949236'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'judge.com'
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
            page = 0
            while True:
                url = 'https://careers-judge.icims.com/jobs/search?ss=1&hashed=-625949236&in_iframe=1&pr='+str(page)
                page = page + 1
                print("collecting page " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.findAll('a', {'class': 'iCIMS_Anchor'})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = link.get('href')
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                try:
                                    jobDetail = BeautifulSoup(jobres.text, 'lxml')
                                    jobObj['title'] = link.find('h2').text.replace('\n', '').replace('\r', '').strip()
                                    jobObj['location'] = jobDetail.find('div', {'class': 'col-xs-6 header left'}).text.replace('\n', '').replace('\r', '').replace('Job Locations', '').strip()
                                    jobObj['description'] = str(jobDetail.find('div', {'class': 'iCIMS_JobContent'}))
                                except:
                                    pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                    else:
                        print("Job not Found!")
                        break

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs[0])
