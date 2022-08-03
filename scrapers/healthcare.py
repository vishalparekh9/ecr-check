import json

import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'GE_HEALTHCARE'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.gecareers.com/'

        self.payload = '{"lang":"en_global","deviceType":"desktop","country":"global","pageName":"Healthcare-digital-jobs","ddoKey":"eagerLoadRefineSearch","sortBy":"Most recent","subsearch":"","from":0,"jobs":true,"counts":true,"all_fields":["category","country","state","city","business","experienceLevel"],"pageType":"landingPage","size":1000,"rk":"l-healthcaredigitaljobs","clearAll":true,"jdsource":"facets","isSliderEnable":false,"pageId":"page2770-prod","siteType":"healthcare","location":"","keywords":"","global":true,"selected_fields":{"category":["Digital Technology / IT","Project Management","Product Management"],"country":["United States of America"]},"sort":{"order":"desc","field":"postedDate"},"rkstatus":true,"s":"1"}'
        self.getHeaders = {
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'gecareers.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def get_request(self, url):
        try:
            res = self.session.request("POST", url, headers=self.getHeaders, data=self.payload)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            url = 'https://jobs.gecareers.com/healthcare/widgets'
            isloaded, res = self.get_request(url)
            if isloaded:
                try:
                    datas = res.json()["eagerLoadRefineSearch"]["data"]["jobs"]
                    if datas:
                        for data in datas:
                            jobObj = deepcopy(self.obj)
                            url = str("https://jobs.gecareers.com/healthcare/global/en/job/"+str(data['jobId'])+"/"+str(data['title']).replace(" ", "-")+"").strip()
                            jobObj["url"] = url
                            jobObj["title"] = str(data['title'])
                            jobObj["location"] = str(data['multi_location'])
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                try:
                                    jobDesc = BeautifulSoup(res.text, "lxml")
                                    jobDetails = jobDesc.find("script", {"type": "application/ld+json"}).text
                                    stud_obj = json.loads(jobDetails)
                                    from html import unescape
                                    stud_obj = str(stud_obj["description"])
                                    unescaped = unescape(stud_obj)
                                    jobObj['description'] = str(unescaped)
                                except:
                                    pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['title'])
                except Exception as e:
                    print(e)
                    self.iserror = True
                    pass
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))




