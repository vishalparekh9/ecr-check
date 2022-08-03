import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'ALTIMETRIK_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://altimetrik.com'

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
        self.domain = 'altimetrik.com'
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
                url = 'https://careers.altimetrik.com/go/US-Jobs/587344/'
                page += 25
                if page > 0:
                    url = f'https://careers.altimetrik.com/go/US-Jobs/587344/{page}'
                print("collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    links = data.find_all("tr", {"class": "data-row"})
                    if len(links) == 0: break
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            try:
                                l = link.find("a").get("href")
                                url = f"https://careers.altimetrik.com{l}"
                                jobObj['title'] = link.find("a").text.replace("\r", "").replace("\n", "").strip()
                                jobObj['url'] = url
                                loc = link.find("span", {"class": "jobLocation"}).text.replace("\r", "").replace("\n", "").strip()
                                jobObj['location'] = loc
                                isloaded, res = self.get_request(url)
                                if isloaded:
                                    data = BeautifulSoup(res.text, "lxml")
                                    jd = data.find("div", {"class": "content"})
                                    jobObj['description'] = str(jd)
                            except:
                                pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['title'])
                else:
                    print("Job Not Found")
                    break
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))