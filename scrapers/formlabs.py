import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'FORMLABS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'http://formlabs.com/'

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
        self.domain = 'formlabs.com'
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
            url = 'https://careers.formlabs.com/all-open-roles/'
            print()
            print(url)
            print()
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find("div", {"class": "rt-tbody"}).find_all("div", {"class": "rt-tr-group"})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = str("https://careers.formlabs.com" + link.find("a").get("href"))
                        jobObj['url'] = str(url)
                        jobObj['title'] = str(link.find("a").text)
                        jobObj['location'] = str(link.find("div", {"class": "rt-td location"}).text)
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            data = BeautifulSoup(res.text, "lxml")
                            jobObj['description'] = str(data.find("div", {"class": "Grid_cell__TVgMH Grid_small-24__eNIm2 Grid_medium-11__BMmpr Grid_small-offset-0__Q1Roi Grid_medium-offset-0__itTru Grid_large-offset-0__yalGQ"}))
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