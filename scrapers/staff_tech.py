import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'STAFF_TECH'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobs.staff-tech.net/'

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
        self.domain = 'staff-tech.net'
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
            url = 'https://jobs.staff-tech.net'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find("tbody").find_all("tr")
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        if link.find("a").get("href") is not None:
                            url = link.find("a").get("href")
                            jobObj['url'] = url
                            print(url)
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, "lxml")
                                jobObj['title'] = data.find("div", {"id": "jobdetailspage"}).find("h1").text.replace("\r", "").replace("\n", "").strip()
                                loc = data.find('div', {'class': 'acjb-lineheig'})
                                if loc is not None:
                                    jobObj['location'] = loc.text.replace("\r", "").replace("\n", "").replace("Location", "").strip()
                                else:
                                    jobObj['location'] = "United States"

                                jobDesc = data.find("div", {"id": "jobdetailspage"})
                                jobObj['description'] = str(jobDesc)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)

                            else:
                                ispage = False
                                break
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



