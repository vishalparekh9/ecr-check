import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'NATIONALGENERAL'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://nationalgeneral.com/'

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
        self.domain = 'nationalgeneral.com'
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
            page = -1
            ispage = True
            while ispage:
                page = page + 1
                url = 'https://careers.nationalgeneral.com/en-US/search?keywords=&location=&pagenumber='+str(page)+''
                print()
                print(url)
                print()
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    links = data.find_all("tr", {"class": "job-result"})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = str("https://careers.nationalgeneral.com") + link.find("a").get("href")
                            jobObj['url'] = url
                            jobObj['title'] = link.find("a").text.replace("\r", "").replace("\n", "").strip()
                            jobObj['location'] = link.find("div", {"class": "job-location-line"}).text.replace("\r", "").replace("\n", "").strip()
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                jobDetails = BeautifulSoup(res.text, "lxml")
                                jobObj['description'] = str(jobDetails.find("div", {"id": "jdp-job-description-section"}))
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        ispage = False
                        break
                else:
                    print("Job Not Found")
            else:
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)