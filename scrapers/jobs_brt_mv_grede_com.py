
import json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOBS_BRT_MV_GREDE'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.grede.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'Content-Type': 'application/json'
        }

        self.session = requests.session()
        self.domain = 'grede.com'
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
            url1 = f'https://j.brt.mv/ax.do?refresh=true&portalGK=30056'
            print(url1)
            isloaded1, res1 = self.get_request(url1)
            if isloaded1:
                data1 = BeautifulSoup(res1.text, "lxml")
                links1 = data1.find_all("tr", {"class": "BMData"})
                if len(links1) > 0:
                    for rd1 in links1:
                        url2 = "https://j.brt.mv/" + rd1.find("a").get("href")
                        isloaded2, jobres2 = self.get_request(url2)
                        if isloaded2:
                            try:
                                data2 = BeautifulSoup(jobres2.text, "lxml")
                                links2 = data2.find_all("tr", {"class": "BMData"})
                                if len(links2) > 0:
                                    for rd2 in links2:
                                        jobObj = deepcopy(self.obj)
                                        jobObj['title'] = rd2.find_all("td")[1].text
                                        jobObj['location'] = rd2.find_all("td")[2].text
                                        url3 = "https://j.brt.mv/" + rd2.find("a").get("href")
                                        jobObj['url'] = url3
                                        isloaded3, jobres3 = self.get_request(url3)
                                        if isloaded3:
                                            try:
                                                jobData = BeautifulSoup(jobres3.text, "lxml")
                                                jd = jobData.find('div', {'class': 'panel panel-default'})
                                                jobObj['description'] = str(jd)
                                                if jobObj['title'] != '' and jobObj['url'] != '':
                                                    self.allJobs.append(jobObj)
                                                    print(jobObj)
                                            except Exception as e:
                                                print(e)
                                                pass
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