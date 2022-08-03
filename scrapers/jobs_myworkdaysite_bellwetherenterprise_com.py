
import json
import requests
from copy import deepcopy
from bs4 import BeautifulSoup
from index import get_obj

# Token
token = 'JOBS_MYWORKDAYSITE_BELLWETHERENTERPRISE'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.bellwetherenterprise.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'Content-Type': 'application/json',
            'Cookie': 'PLAY_SESSION=24c09e24ebf752236cffaf07b7b9ab239851956f-instance=wd3prvps0007c; TS014c1515=01f629630482c050efab2e28da227574128acac4c44376b62f486657c9fb5d844bdf0bf7115060a39833cf8c05ed3308db4175235b; wd-browser-id=eebac404-c9e9-42af-b8dc-a4444559e798; wday_vps_cookie=2166789642.58930.0000'
        }

        self.session = requests.session()
        self.domain = 'bellwetherenterprise.com'
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
                url = f'https://wd5.myworkdaysite.com/wday/cxs/enterprisecommunity/BellwetherCareers/jobs'

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
                            try:
                                jobObj = deepcopy(self.obj)
                                jobObj['title'] = rd['title']
                                jobObj['location'] = str(rd['locationsText'])
                                url = "https://wd5.myworkdaysite.com/wday/cxs/enterprisecommunity/BellwetherCareers" + str(rd['externalPath'])
                                jobObj['url'] = url
                                isloaded, jobres = self.get_requests(url)
                                if isloaded:
                                    jobDetails = BeautifulSoup(jobres.text, "lxml").find("body").text
                                    jsonJobDesc = json.loads(str(jobDetails))
                                    jobObj['description'] = str(jsonJobDesc['jobPostingInfo']['jobDescription'])
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                            except Exception as e:
                                pass
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