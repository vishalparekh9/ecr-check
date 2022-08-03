import json

import requests
from copy import deepcopy
from bs4 import BeautifulSoup
from index import get_obj

# Token
token = 'GORE_CAREER_JOBS_TALEO'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://wlgore.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=140480292&iniurl.src=CWS-10860'

        self.getHeaders = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://wlgore.taleo.net',
            'Referer': 'https://wlgore.taleo.net/careersection/2/jobsearch.ftl?lang=en&src=CWS-10860',
            'tzname': 'los/angeles',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'locale=en'
        }
        self.session = requests.session()
        self.domain = 'gore.com'
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

    def post_request(self, url, page):
        try:
            payload = "{\"multilineEnabled\":false,\"sortingSelection\":{\"sortBySelectionParam\":\"1\",\"ascendingSortingOrder\":\"false\"},\"fieldData\":{\"fields\":{\"LOCATION\":\"\",\"KEYWORD\":\"\",\"JOB_NUMBER\":\"\"},\"valid\":true},\"filterSelectionParam\":{\"searchFilterSelections\":[{\"id\":\"LOCATION\",\"selectedValues\":[]},{\"id\":\"JOB_FIELD\",\"selectedValues\":[]},{\"id\":\"JOB_SHIFT\",\"selectedValues\":[]}]},\"advancedSearchFiltersSelectionParam\":{\"searchFilterSelections\":[{\"id\":\"EMPLOYEE_STATUS\",\"selectedValues\":[]},{\"id\":\"JOB_SCHEDULE\",\"selectedValues\":[]}]},\"pageNo\":"+str(page)+"}"

            res = self.session.request("POST", url=url, headers=self.getHeaders, data=payload)
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
                isloaded, res = self.post_request(self.baseUrl, page)
                if isloaded:
                    links = res.json()['requisitionList']
                    if len(links) > 0:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = f"https://wlgore.taleo.net/careersection/2/jobdetail.ftl?job={link['jobId']}&iniurl.src=CWS-10860&tz=GMT%2B05%3A30&tzname=los%2Fangeles"
                            jobObj['url'] = url
                            jobObj['title'] = link['column'][0]
                            jobObj['location'] = link['column'][1].replace('["', '').replace('"]', '')
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, 'lxml')
                                jobDesc = str(data.find('div', {'class': 'columnfull'}))
                                if jobDesc:
                                    jobObj['description'] = jobDesc
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                    else:
                        isPage = False
                        break
                else:
                    print('No Job Data Found!')
                    isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
