import json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'CAREERS_MICROSOFT_JOBS_ALL'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.microsoft.com/us/en/search-results'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'microsoft.com'
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
        page = -10
        isPage = True
        while isPage:
            page = page + 10
            print("Collecting for page ", page)
            url = f'https://careers.microsoft.com/us/en/search-results?from={page}&s=1'
            print(url)
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find_all("script", {"type": "text/javascript"})
                for link in links:
                    if "widgetApiEndpoint" in str(link.text):
                        if link is not None:
                            jsonData = str(link.text.replace('/*<!--*/ var phApp = phApp || ', '').replace(';', '').replace('/*--&gt*/', '').replace("/*-->*/", ""))
                            jsonRawData = json.loads(jsonData.split('"eagerLoadRefineSearch":')[1].split("} phApp.sessionParams")[0])['data']
                            if len(jsonRawData['jobs']) > 0:
                                for rd in jsonRawData['jobs']:
                                    jobObj = deepcopy(self.obj)
                                    jobObj['title'] = rd['title']
                                    jobObj['location'] = str(rd['location'])
                                    url = str(rd['applyUrl']).replace("/apply", "")
                                    jobObj['url'] = url
                                    if isloaded:
                                        try:
                                            jd = rd['description'] + "\n\n" + rd['jobQualifications'] + "\n\n" + rd['jobResponsibilities'] + "\n\n" + rd['jobSummary']
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


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))

