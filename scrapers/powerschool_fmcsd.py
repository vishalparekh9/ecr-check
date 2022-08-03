import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'POWERSCHOOL_FMCSD'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.fmcsd.org'

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
        self.domain = 'fmcsd.org'
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
            url = 'https://ats5.atenterprise.powerschool.com/ats/job_board?COMPANY_ID=JA002638&REPRESENTATIVE_COMPANY_ID=JA003085'
            print(url)
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find("tbody").find_all("tr")
                for link in links:
                    if link.find("td") is not None:
                        jobObj = deepcopy(self.obj)
                        url = "https://ats5.atenterprise.powerschool.com" + str(link.find_all("td")[0].find("a").get("href"))
                        jobObj['title'] = link.find_all("td")[3].text
                        jobObj['location'] = link.find_all("td")[4].text
                        jobObj['url'] = "" + str(url)
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            data = BeautifulSoup(res.text, 'lxml')
                            jobObj['description'] = str(data.find("div", {"class": "message job-description"})) + "<br />" + str(data.find("div", {"class": "job-items"}))
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
            else:
                print("Job Not Found!")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)