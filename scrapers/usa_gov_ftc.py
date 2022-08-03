import json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'USA_CAREER_JOBS_FTC_GOV'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://ftc.gov'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest'
        }

        self.session = requests.session()
        self.domain = 'ftc.gov'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def get_request(self, url, page, isJson):
        try:
            if isJson:
                payload = {
                    "JobTitle": [],
                    "GradeBucket": [],
                    "JobCategoryCode": [],
                    "JobCategoryFamily": [],
                    "LocationName": [],
                    "PostingChannel": [],
                    "Department": [],
                    "Agency": [],
                    "PositionOfferingTypeCode": [],
                    "TravelPercentage": [],
                    "PositionScheduleTypeCode": [],
                    "SecurityClearanceRequired": [],
                    "PositionSensitivity": [],
                    "ShowAllFilters": [],
                    "HiringPath": [],
                    "SocTitle": [],
                    "MCOTags": [],
                    "CyberWorkRole": [],
                    "CyberWorkGrouping": [],
                    "Keyword": "FTC",
                    "Page": page,
                    "IsAuthenticated": False
                }

                json_object = json.dumps(payload, indent=4)

                res = self.session.request("POST", url, headers=self.getHeaders, data=json_object)
                return True, res
            else:
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
                url = 'https://www.usajobs.gov/Search/ExecuteSearch'
                isloaded, res = self.get_request(url, page, True)
                if isloaded:
                    links = res.json()['Jobs']
                    if len(links) > 0:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = "" + link['PositionURI'].strip()
                            jobObj['url'] = url
                            jobObj['title'] = link['Title'].strip()
                            jobObj['location'] = link['Location'].strip()
                            isloaded, res = self.get_request(url, page, False)
                            if isloaded:
                                data = BeautifulSoup(res.text, 'lxml')
                                jobDesc = str(data.find('div', {'class': 'usajobs-joa-intro--v1-5__container'}))
                                jobObj['description'] = jobDesc
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        isPage = False
                        print("Job Not Found")
                        break

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
