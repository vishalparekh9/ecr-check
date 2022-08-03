
import json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOBS_OUR_CAREER_PAGES_HERRS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.herrs.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'Content-Type': 'application/json'
        }

        self.session = requests.session()
        self.domain = 'herrs.com'
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

    def post_request(self, url, page, company):
        try:
            payload = json.dumps({
                "className": "HostedCareerPage",
                "methodName": "GetSearchResults",
                "methodParms": {
                    "searchBy": {
                        "AND": {
                            "state_abbrev": "",
                            "city": "",
                            "skill_tags": ""
                        },
                        "LIKE": {
                            "description": "",
                            "job_title": ""
                        },
                        "IN": {
                            "postal_code": "",
                            "radius": "0"
                        },
                        "COUNTY": {
                            "postal_code": ""
                        }
                    },
                    "ccpCode": f"{company}"
                }
            })

            res = self.session.request("POST", url=url, headers=self.getHeaders, data=payload)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            company = "hfi"
            url = f'http://hfi.ourcareerpages.com/WebServices/BDHWebServiceDirector.asmx/ProcessRequest'
            print(url)
            isloaded, res = self.post_request(url, 0, company)
            if isloaded:
                data = res.json()['d']['retVals']['job']
                if len(data) > 0:
                    for rd in data:
                        jobObj = deepcopy(self.obj)
                        jobObj['title'] = rd['job_title']
                        jobObj['location'] = rd['city'] + ", " + rd['state_abbrev']
                        job_id = rd['job_id']
                        url = str(f"http://hfi.ourcareerpages.com/JobView.aspx?id={job_id}&jobFeedCode={company}&source={company}")
                        jobObj['url'] = url
                        print(jobObj)
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            try:
                                jobData = BeautifulSoup(jobres.text, "lxml")
                                jd = jobData.find('div', {'class': 'nine columns'})
                                print(jd)
                                jobObj['description'] = str(jd).replace("NBSP", " ")
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                            except Exception as e:
                                print(e)
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