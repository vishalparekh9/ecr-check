import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os
import common as cf
# Token
token = 'DELOITTE'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'http://deloitte.com/'

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
        self.domain = 'deloitte.com'
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
            ispage = True
            while ispage:
                page = page + 10
                print("Coolecting page " + str(page))
                url = 'https://apply.deloitte.com/careers/SearchJobsAJAX?sort=relevancy&s=1&3_133_3=1253,1234,1237,1241,1242,12776712,1248,1250,1251&jobOffset='+str(page)+''
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('article', {"class": "article--result opacity--0"})
                    if links:
                        self.allJobs = []
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            try:
                                url = link.find("a").get("href")
                                jobObj['url'] = url
                                jobObj['title'] = link.find('h3').text.replace("\r", "").replace("\n", "").strip()
                                loc = link.find('div', {"class": "article__header__text__subtitle"}).text.replace("\r", "").replace("\n", "").strip().split("|")[2]
                                jobObj['location'] = " ".join(loc.split())
                                isloaded, res = self.get_request(url)
                                if isloaded:
                                    data = BeautifulSoup(res.text, 'lxml')
                                    jobDesc = data.find("div", {"class": "container--boxed"})
                                    jobObj['description'] = str(jobDesc)
                            except:
                                pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                        cf.insert_rows(self.allJobs, self.site, self.iserror, self.domain, False)
                    else:
                        ispage = False

                else:
                    ispage = False
                    print("Job Not Found")
            else:
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)



