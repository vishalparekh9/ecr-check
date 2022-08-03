
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'DIZZION_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.dizzion.com'

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
        self.domain = 'dizzion.com'
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
            url = 'https://www.dizzion.com/company/careers/'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find("div", {"id": "list-icon-benefits"}).find_all("div", {"class": "col-sm-4"})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        try:
                            url = str(link.find("a").get("href"))
                            jobObj['url'] = url
                            jobObj['title'] = link.find("h4").text.replace("\n", "").replace("\r", "").replace("Job Opening", "").strip()
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, 'lxml')
                                jobObj['location'] = data.find('div', {'class': 'col-sm-12'}).find_all("p")[2].text.replace("\n", "").replace("\r", "").replace("LOCATION | ", "").strip()
                                jobDesc = str(data.find('div', {'class': 'container'}))
                                if jobDesc:
                                    jobObj['description'] = jobDesc
                        except:
                            pass
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))