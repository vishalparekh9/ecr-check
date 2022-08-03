import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

# Token
token = 'AAUW'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.aauw.org/about/careers/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://www.aauw.org/about/careers/',
            'clientId': '8a7883d0798f66af017a11c59c80366f',
            'parentUrl': 'https://www.aauw.org/about/careers/',
            'gns': '',
        }
        self.session = requests.session()
        self.domain = 'aauw.org'
        self.allJobs = []
        self.obj = deepcopy(get_obj())
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
            jobid = ""
            url = 'https://recruitingbypaycor.com/career/CareerHome.action?clientId=8a7883d0798f66af017a11c59c80366f&parentUrl=https%3A%2F%2Fwww.aauw.org%2Fabout%2Fcareers%2F&gns='
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find('table', {'id': 'gnewtonCareerHome'}).findAll('div',
                                                                                {'class': 'gnewtonCareerGroupRowClass'})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = link.find('a').get('href')
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            jobDetail = BeautifulSoup(jobres.text, 'lxml')
                            jobObj['title'] = link.find('a').text.replace('\n', '').replace('\r', '').strip()
                            jobObj['location'] = link.find('div', {
                                'class': 'gnewtonCareerGroupJobDescriptionClass'}).text.replace('\n', '').replace('\r',
                                                                                                                  '').strip()
                            jobObj['description'] = str(jobDetail.find('table', {'id': 'gnewtonJobDescription'}))
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
