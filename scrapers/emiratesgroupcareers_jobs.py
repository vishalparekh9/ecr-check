import json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'EMIRATES_GROUP_CAREERS_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.emiratesgroupcareers.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'emiratesgroupcareers.com'
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

            url = f'https://www.emiratesgroupcareers.com/api/v1/jobs'
            print(url)
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find("p").text
                jsonData = json.loads(links)['data']
                if len(jsonData) > 0:
                    for rd in jsonData:
                        jobObj = deepcopy(self.obj)
                        jobObj['title'] = rd['title']
                        jobObj['location'] = rd['location']
                        jobObj['url'] = rd['url']
                        qualifications = rd['qualifications']
                        jobObj['description'] = str(rd['description'] + "<br />" + qualifications + "<br />" + rd['salarybenefits'])
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))