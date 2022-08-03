import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'AEYEINC'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.aeyeinc.com/'

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
        self.domain = 'aeyeinc.com'
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
            url = 'https://boards-api.greenhouse.io/v1/boards/aeyeinc/jobs'
            isloaded, res = self.get_request(url)
            if isloaded:
                if "jobs" in str(res.json()):
                    for data in res.json()["jobs"]:
                        if data:
                            jobObj = deepcopy(self.obj)
                            url = data['absolute_url']
                            jobObj['url'] = url
                            jobObj['domain'] = self.domain
                            jobObj['title'] = data['title']
                            if data['location']['name']:
                                jobObj['location'] = data['location']['name']
                            else:
                                jobObj['location'] = "United States"

                            isloaded, res = self.get_request('https://boards.greenhouse.io/embed/job_app?for=aeyeinc&token='+url.split('gh_jid=')[1]+'&b=https%3A%2F%2Fwww.aeyeinc.com%2Fcareers')

                            if isloaded:
                                jobDetails = BeautifulSoup(res.text, "lxml")
                                import json
                                jsonJobDesc = json.loads(str(jobDetails.find("script", {"type": "application/ld+json"}).text))
                                jobObj['description'] = str(jsonJobDesc['description'])
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                else:
                    print("Job Not Found")
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
