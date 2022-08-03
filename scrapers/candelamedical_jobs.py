
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'CANDELA_MEDICAL_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.candelamedical.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=SYNEMEDI',
            #'Cookie': 'JSESSIONID=2F2914122C369B9B4F2B281B7415155F'
        }
        self.session = requests.session()
        self.domain = 'candelamedical.com'
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
            url = 'https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=SYNEMEDI'
            isloaded, res = self.get_request(url)
            page = -10
            ispage = True
            while ispage:
                page = page + 10
                url = 'https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=SYNEMEDI&next&rowFrom='+str(page)+'&act=null&sortColumn=null&sortOrder=null'
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('div', {"class": "oracletaleocwsv2-accordion oracletaleocwsv2-accordion-expandable clearfix"})
                    print(len(links))
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = link.find("a").get("href")
                            jobObj['url'] = url
                            jobObj['title'] = link.find('h4').text.replace("\r", "").replace("\n", "").strip()
                            loc = link.find('div', {"class": "oracletaleocwsv2-accordion-head-info"}).find_all("div")[1].text.replace("\r", "").replace("\n", "").strip()
                            jobObj['location'] = " ".join(loc.split())
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, 'lxml')
                                jobDesc = data.find("div", {"name": "cwsJobDescription"})
                                jobObj['description'] = str(jobDesc)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj['location'])
                    else:
                        ispage = False
                        break
                else:
                    print("Job Not Found")
                    ispage = False
            else:
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))