import json
import re

import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'GRAB_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.nera.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'nera.com'
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
            url = f'https://grab.careers/jobs/?keyword='
            print(url)
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                link = data.find('main', {'id': 'main'}).find("script").text
                if link is not None:
                    jsonData = str(link.replace("window.jobsList = ", ""))
                    jsonRawData = json.loads(jsonData)
                    if len(jsonRawData) > 0:
                        for rd in jsonRawData:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = rd['title']
                            jobObj['location'] = str(rd['country'])
                            reference = str(rd['reference']).strip()
                            url = f"https://grab.careers/jobs/job-details/?id={reference}"
                            jobObj['url'] = url
                            isloaded, jres = self.get_request(url)
                            if isloaded:
                                try:
                                    jobData = BeautifulSoup(jres.text, "lxml")
                                    jd = jobData.find('div', {'class': 'job-cta'}).find('a').get("href")
                                    jd = jd.replace("/apply?source=GrabCareers", "")
                                    print(jd)
                                    isloaded, jobres = self.get_request(jd)
                                    if isloaded:
                                        jobDetails = BeautifulSoup(jobres.text, "lxml")
                                        jsonJobDesc = json.loads(str(jobDetails.find("script", {"type": "application/ld+json"}).text))
                                        jobObj['description'] = str(jsonJobDesc['description'])
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                            print(jobObj)

                                except Exception as e:
                                    print(e)
                                    pass

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)
