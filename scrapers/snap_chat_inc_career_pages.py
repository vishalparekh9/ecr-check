import json
import requests
from copy import deepcopy
from bs4 import BeautifulSoup
from index import get_obj

# Token
token = 'SNAP_WORKDAY_JOBS_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.snap.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        }

        self.session = requests.session()
        self.domain = 'snap.com'
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
            url = "https://www.snap.com/api/jobs"
            isloaded, res = self.get_request(url)
            if isloaded:
                data = res.json()['data']['Report_Entry']
                if len(data) > 0:
                    for rd in data:
                        try:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = rd['title']
                            jobObj['location'] = str(rd['primary_location'])
                            url = str(rd['absolute_url'])
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                jobDetails = BeautifulSoup(jobres.text, "lxml")
                                jsonJobDesc = json.loads(
                                    str(jobDetails.find("script", {"type": "application/ld+json"}).text))
                                jobObj['description'] = str(jsonJobDesc['description'])
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                        except (Exception, AttributeError, KeyError, ValueError) as e :
                            pass

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)
