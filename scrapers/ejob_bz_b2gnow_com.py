
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOB_BOARD_EJOB_BZ_B2GNOW_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://b2gnow.com/'

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
        self.domain = 'b2gnow.com'
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
            url = 'https://ejob.bz/CompanyPortal.do?refresh=true&companyGK=19703&portalGK=2910'
            isloaded, res = self.get_request(url)
            if isloaded:
                linksData = BeautifulSoup(res.text, "lxml")
                links = linksData.find_all("tr", {"class": "BMData"})
                if links:
                    for link in links:
                        if link.find("a") is not None:
                            jobObj = deepcopy(self.obj)
                            url = "https://ejob.bz/" + link.find("a").get("href")
                            jobObj['url'] = url
                            jobObj['title'] = link.find("strong").text.strip()
                            jobObj["location"] = link.find_all("td")[1].text.strip()
                            if jobObj["location"] == ".,":
                                jobObj["location"] = "United States"
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                jobDetails = BeautifulSoup(res.text, "lxml")
                                desc = str(jobDetails.find("div", {"class": "portalsubsection bmportalrequirementdetails"}))
                                jobObj['description'] = str(desc)
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