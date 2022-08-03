import json

import requests
from copy import deepcopy

from bs4 import BeautifulSoup

from index import get_obj

# Token
token = 'REGIONS_WORKDAY_JOBS_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.regions.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'Content-Type': 'application/json'
        }

        self.session = requests.session()
        self.domain = 'regions.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def get_request(self, url, payload):
        try:
            res = self.session.request("POST", url=url, headers=self.getHeaders, data=payload)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def get_requests(self, url):
        try:
            res = self.session.get(url, headers=self.getHeaders)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            page = 0
            isPage = True
            while isPage:
                page = page + 1
                print("Collecting for page ", page)
                url = 'https://regions.wd5.myworkdayjobs.com/wday/cxs/regions/regions_careers/jobs'

                payload = json.dumps({
                    "appliedFacets": {},
                    "limit": 20,
                    "offset": page,
                    "searchText": ""
                })

                isloaded, res = self.get_request(url, payload)
                if isloaded:
                    data = res.json()['jobPostings']
                    if len(data) > 0:
                        for rd in data:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = rd['title']
                            jobObj['location'] = str(rd['locationsText'])
                            url = "https://regions.wd5.myworkdayjobs.com/en-US/Regions_Careers" + str(rd['externalPath'])
                            jobObj['url'] = url
                            isloaded, jobres = self.get_requests(url)
                            if isloaded:
                                jobDetails = BeautifulSoup(jobres.text, "lxml")
                                jsonJobDesc = str(jobDetails.find("meta", {"property": "og:description"}).get("content"))
                                jobObj['description'] = str(jsonJobDesc)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        print("No Jobs")
                        isPage = False
                        break
            else:
                print("Job Not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)