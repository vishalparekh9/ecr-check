import json
import requests
from copy import deepcopy
from bs4 import BeautifulSoup
from index import get_obj
import re

# Token
token = 'MY_WORKDAY_JOBS_ARROW_COM'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://arrow.wd1.myworkdayjobs.com/wday/cxs/arrow/AC/jobs'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'Content-Type': 'application/json'
        }

        self.session = requests.session()
        self.domain = 'arrow.com'
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
            jobtitles = []
            
            page = -20
            isPage = True
            while isPage:
                page = page + 20
                print("Collecting for page ", page)
                url = f'https://arrow.wd1.myworkdayjobs.com/wday/cxs/arrow/AC/jobs'

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
                            try:
                                if rd['title'] not in jobtitles:
                                    jobtitles.append(rd['title'])
                                    jobObj['title'] = rd['title']
                                    jobObj['location'] = str(rd['locationsText'])
                                    url = "https://arrow.wd1.myworkdayjobs.com/wday/cxs/arrow/AC" + str(rd['externalPath'])
                                    jobObj['url'] = url
                                    isloaded, jobres = self.get_requests(url)
                                    if isloaded:
                                        jsonJobDesc = jobres.json()['jobPostingInfo']['jobDescription']
                                        jobObj['description'] = re.sub(r'[^\x00-\x7f]', r' ', str(jsonJobDesc))
                                else:
                                    isPage = False
                                    break
                            except:
                                pass
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