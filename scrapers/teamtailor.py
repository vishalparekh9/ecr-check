
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'CRIADVANTAGE_TEAM_TAILOR'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://criadvantage.com'

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
        self.domain = 'criadvantage.com'
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
            url = 'https://criadvantage.teamtailor.com/jobs'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find_all("li", {"class": "w-full"})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        try:
                            url = link.find("a").get("href")
                            jobObj['title'] = link.find("a").find("span").text.replace("\r", "").replace("\n", "").strip()
                            jobObj['url'] = url
                            loc = link.find("div", {"class": "mt-1 text-md"}).text.replace("\r", "").replace("\n", "").strip().split("·")
                            jobObj['location'] = loc[1]
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, "lxml")
                                jd = data.find("div", {"class": "mx-auto max-w-[750px] prose font-company-body overflow-hidden"})
                                jobObj['description'] = str(jd)
                        except:
                            pass
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj['url'])
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))




