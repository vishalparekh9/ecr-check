
import json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'VERITIVCORP_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://veritivcorp.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'veritivcorp.com'
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
            page = -10
            isPage = True
            while isPage:
                page = page + 10
                print("Collecting for page ", page)
                url = f'https://careers.veritivcorp.com/us/en/c/information-technology-jobs?from={page}&s=1'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    link = data.find("script", {"type": "text/javascript"}).text
                    if "widgetApiEndpoint" in str(data):
                        if link is not None:
                            jsonData = str(link.replace('/*&lt;!--*/ var phApp = phApp || ', '').replace(';', '').replace('/*--&gt*/', ''))
                            jsonRawData = json.loads(jsonData.split("phApp.ddo = ")[1].split("phApp.experimentData")[0])['eagerLoadRefineSearch']['data']
                            if len(jsonRawData['jobs']) > 0:
                                for rd in jsonRawData['jobs']:
                                    jobObj = deepcopy(self.obj)
                                    jobObj['title'] = rd['title']
                                    jobObj['location'] = str(rd['country'] + ", " + rd['cityState'])
                                    url = str(rd['applyUrl']).replace("/apply", "")
                                    jobObj['url'] = url
                                    isloaded, jobres = self.get_request(url)
                                    if isloaded:
                                        try:
                                            jobData = BeautifulSoup(jobres.text, "lxml")
                                            jd = jobData.find('meta', {'property': 'og:description'}).get("content")
                                            jobObj['description'] = str(jd)
                                            if jobObj['title'] != '' and jobObj['url'] != '':
                                                self.allJobs.append(jobObj)
                                                print(jobObj)
                                        except Exception as e:
                                            print(e)
                                            pass
                            else:
                                print("Job Not Found")
                                isPage = False
                                break
                        else:
                            print("Job Not Found")
                            isPage = False
            else:
                print("Job Not Found")
                isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))