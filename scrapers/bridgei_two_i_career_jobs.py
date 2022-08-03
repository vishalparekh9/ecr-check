import requests
from copy import deepcopy
import json
from bs4 import BeautifulSoup
from index import get_obj

# Token
token = 'SAP_CONCUR_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.concur.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'concur.com'
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
            page = -25
            isPage = True
            while isPage:
                page = page + 25
                url = f'https://jobs.sap.com/search/?q=Concur&startrow={page}'
                print(f"Collecting for page {page}")
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    for jdata in data.find_all("tr", {"class": "data-row clickable"}):
                        if jdata is not None:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = jdata.find("a").text.replace("\r", "").replace("\n", "").strip()
                            url = 'https://jobs.sap.com' + str(jdata.find("a").get("href"))
                            jobObj['location'] = jdata.find("span", {"class": "jobLocation"}).text.replace("\r", "").replace("\n", "").strip()
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                jobdata = BeautifulSoup(jobres.text, "lxml")
                                jobDesc = jobdata.find("div", {"class": "joblayouttoken displayDTM marginTopNone marginBottomNone marginRightNone marginLeftNone"})
                                jobObj['description'] = str(jobDesc)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        isPage = False
                        break
            else:
                isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)