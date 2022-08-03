import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj

# Token
token = 'DIGITAL_CAREERS_INFOSYS_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://digitalcareers.infosys.com/'

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
        self.domain = 'infosys.com'
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
            isloaded, res = self.get_request('https://digitalcareers.infosys.com/infosys/global-careers?job_type=graduate&location=USA')
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('a', {'class': 'job editable-cursor'})
                for link in links:
                    jobObj = deepcopy(self.obj)
                    url = '' + str(link.get("href"))
                    jobObj['url'] = url
                    jobObj['title'] = str(link.find('div', {"class": "job-title"}).text.strip())
                    jobObj['location'] = str(link.find('div', {'class': 'job-location js-job-city'}).text.strip())
                    isloaded, res = self.get_request(url)
                    if isloaded:
                        jobDetails = BeautifulSoup(res.text, 'lxml')
                        jobObj['description'] = str(jobDetails.find('div', {'class': 'description-page-right'}))
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)
                else:
                    print('No Job Data Found!')
                    isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))