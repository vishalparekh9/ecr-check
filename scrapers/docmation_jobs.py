import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

token = 'DOCMATION_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://docmation.com/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'cookie': '_gid=GA1.2.2001214597.1649404168; _ga_TJK78EQ1E4=GS1.1.1649417076.2.0.1649417076.0; _ga_G2LRJ0L6V7=GS1.1.1649417077.2.0.1649417077.0; _ga=GA1.2.1398922321.1649404167'
        }
        self.session = requests.session()
        self.domain = 'docmation.com'
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
            url = 'https://docmation.com/current-openings/'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find('div', {'id': 'tab-92ffe61c-0cc1-4'}).find_all('div', {'class': 'rt-accordion-item'})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        jobObj['title'] = link.find('h4').text.replace('\n', '').replace('\r', '').strip()
                        jobObj['url'] = url + '?' + jobObj['title']
                        jobObj['location'] = "United States"
                        jobObj['description'] = str(link.find('div', {'class': 'rt-accordion-item-body'}))
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
