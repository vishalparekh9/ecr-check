import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'TPA_TECHNOLOGIES'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://tpatechnologies.com/'

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
        self.domain = 'tpatechnologies.com'
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
            jobIds = []

            page = -1
            ispage = True
            while ispage:
                page = page + 1
                url = 'https://tpatechnologies.com/search-jobs?page='+str(page)+''
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    links = data.find("tbody").find_all("tr")
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = str("https://tpatechnologies.com" + link.find("td", {"class": "title"}).find("a").get("href"))
                            jobObj['url'] = url
                            jobObj['title'] = link.find("td", {"class": "title"}).text.replace("\r", "").replace("\n", "").strip()
                            jobObj['location'] = link.find("td", {"class": "location"}).text.replace("\r", "").replace("\n", "").strip()
                            JobId = link.find("td", {"class": "job-id"}).text.replace("\r", "").replace("\n", "").strip()
                            if JobId not in jobIds:
                                jobIds.append(JobId)
                                isloaded, res = self.get_request(url)
                                if isloaded:
                                    data = BeautifulSoup(res.text, "lxml")
                                    jobDesc = data.find("div", {"class": "region region-content"})
                                    jobObj['description'] = str(jobDesc)
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
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



