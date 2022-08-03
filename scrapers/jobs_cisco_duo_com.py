
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

# Token
token = 'JOBS_CISCO_DUO'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://duo.com'

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
        self.domain = 'duo.com'
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
            page = -25
            isPage = True
            while isPage:
                page = page + 25
                isloaded, res = self.get_request(f"https://jobs.cisco.com/jobs/SearchJobs/Duo%20Security?21178=%5B169482%5D&21178_format=6020&listFilterMode=1&projectOffset={page}")
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    aTag = data.find_all('tr')
                    if aTag:
                        for link in aTag:
                            if len(aTag) > 1:
                                if link.find("a") is not None:
                                    jobObj = deepcopy(self.obj)
                                    url = link.find("a").get('href')
                                    jobObj['title'] = link.find('a').text.strip()
                                    jobObj['location'] = link.find('td', {'data-th': 'Location'}).text.strip()
                                    jobObj['url'] = url
                                    isloaded, jobres = self.get_request(url)
                                    if isloaded:
                                        jobDetail = BeautifulSoup(jobres.text, 'lxml')
                                        descs = jobDetail.find('div', {'class': "section_mainbar"})
                                        jobObj['description'] += str(descs)
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                            print(jobObj)
                            else:
                                break
                    else:
                        break
            else:
                print('No Job Data Found!')

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))