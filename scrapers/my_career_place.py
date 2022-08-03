
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'MY_CAREER_PLACE'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://my.career.place/'

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
        self.domain = 'career.place'
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
            url = 'https://my.career.place/static/organizations/mpulse-mobile-ckeofrc8h0wod0mpx2n9zcl2f'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('a', {"class": "title"})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = str("https://my.career.place/static" + link.get("href").replace("..", "")).strip()
                        jobObj['url'] = url
                        jobObj['title'] = link.text.replace("\r", "").replace("\n", "").replace("\t", "").strip()
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            data = BeautifulSoup(res.text, 'lxml')
                            jobObj['location'] = data.find('h3').text.replace("\r", "").replace("\n", "").replace("\t", "").strip()
                            jobDesc = str(data.find('div', {'class': 'container'}))
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



