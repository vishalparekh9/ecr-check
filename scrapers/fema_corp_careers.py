
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'FEMA_CORP_CAREERS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://fema-corp.com'

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
        self.domain = 'fema-corp.com'
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
            url = 'https://www.fema-corp.com/contact/employment'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('div', {"class": "post-teaser filtr-item columns-1 bfm-employment-page-teaser"})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = 'https://www.fema-corp.com' + str(link.find("a", {"class": "button more-link darkcyan"}).get('href'))
                        jobObj['url'] = url
                        jobObj['title'] = link.find('div', {'class': 'position-title'}).text.replace("\r", "").replace("\n", "").strip()
                        jobObj['location'] = link.find('label').text.replace("\r", "").replace("\n", "").replace("[", "").replace("]", "").strip()
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            data = BeautifulSoup(res.text, 'lxml')
                            jobDesc = str(data.find('div', {'class': 'longdescription'}))
                            jobObj['description'] = jobDesc
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)