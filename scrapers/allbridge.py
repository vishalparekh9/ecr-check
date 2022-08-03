import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

token = 'ALLBRIDGE'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://allbridge.com/company/careers/'

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
        self.domain = 'allbridge.com'
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
            url = 'https://allbridge.com/company/careers/'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find('div', {'class': 'current-openings'}).findAll('li')
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = str(link.find('a').get('href'))
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            jobDetail = BeautifulSoup(jobres.text, 'lxml')
                            jobObj['title'] = str(link.find('a').text.replace('\n', '')).replace("\r", "").strip()
                            jobObj['location'] = str(jobDetail.find('p', {'class': 'location'}).text.replace('\n', '').replace('\r', '')).strip()
                            jobObj['description'] = str(jobDetail.find('div', {'class': 'posts'}))

                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                else:
                    print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)
