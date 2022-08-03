import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os
import json
from urllib.parse import urlsplit

# Token
token = 'ISOLVEDHIRE_AXXEUM_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://axxeum.isolvedhire.com/jobs/'

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
        self.domain = 'axxeum.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
        self.host = "{0.scheme}://{0.netloc}".format(urlsplit(self.baseUrl))
   
    def get_request(self, url):
        try:
            res = self.session.get(url, headers=self.getHeaders)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find_all("a", {"class": "list-group-item strip-side-borders"})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = link.get("href")
                        if 'http' not in url:
                            url = self.host + url
                        jobObj['url'] = url
                        jobObj['title'] = link.find("h4").text.replace("\r", "").replace("\n", "").strip()
                        jobObj["location"] = link.find("ul", {"class": "listing-details"}).find("li").text.replace("\r", "").replace("\n", "").strip()

                        isloaded, res = self.get_request(url)
                        if isloaded:
                            jobDetails = BeautifulSoup(res.text, "lxml")
                            try:
                                desc = str(jobDetails.find("script", {"type": "application/ld+json"}).text)
                                jsond = json.loads(desc)
                                jobObj['description'] = str(jsond["description"])
                            except:
                                pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))