import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

token = 'EUROFINS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.smartrecruiters.com/Eurofins?search=united%20states'

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
        self.domain = 'eurofins.com'
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
            url = 'https://careers.smartrecruiters.com/Eurofins?search=united%20states'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find('div', {'class': 'openings-body js-openings'}).findAll('section', {'class': 'openings-section opening opening--grouped js-group'})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = str(link.find('a').get('href'))
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            jobDetail = BeautifulSoup(jobres.text, 'lxml')
                            jobObj['title'] = str(link.find('h4').text.replace('\n', '')).replace("\r", "").strip()
                            jobObj['location'] = str(jobDetail.find('li').text.replace('\n', '').replace('\r', '')).strip()
                            jobObj['description'] = str(jobDetail.find('main', {'class': 'jobad-main job'}))

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
