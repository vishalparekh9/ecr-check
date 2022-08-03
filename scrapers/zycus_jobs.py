import re

import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'ZYCUS_CAREERS_GH'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.zycus.com/'

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
        self.domain = 'zycus.com'
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
            page = 0
            isPage = True
            t = None
            isloaded, res = self.get_request("https://zycus.skillate.com")
            if isloaded:
                soup = BeautifulSoup(res.text, "lxml")
                z = soup.find("script", {"src": re.compile(".*buildManifest.js.*")})
                t = z.get("src").split("/_next/static/")[1].split("/")[0]

            if t is not None:
                while isPage:
                    url = f'https://zycus.skillate.com/_next/data/{t}/jobs.json?page={page}&pageSize=10&department=&location=&title=&sortBy=&orderBy=ASC'
                    isloaded, res = self.get_request(url)
                    if isloaded:
                        mainData = res.json()['pageProps']['jobsData']['rows']
                        if len(mainData) > 0:
                            for data in res.json()['pageProps']['jobsData']['rows']:
                                jobObj = deepcopy(self.obj)
                                url = "https://zycus.skillate.com/jobs/" + str(data['id'])
                                jobObj['url'] = url
                                jobObj['title'] = data['title']
                                jobObj['location'] = data['location']
                                isloaded, res = self.get_request(url)
                                if isloaded:
                                    data = BeautifulSoup(res.text, 'lxml')
                                    jobDesc = str(data.find('div', {'class': 'chakra-container css-rfo2q1'}))
                                    if jobDesc:
                                        jobObj['description'] = jobDesc
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                            print(jobObj)
                        else:
                            print("Job Not Found")
                            isPage = False
                            break
                    else:
                        print("Job Not Found")
                        isPage = False
                        break
                else:
                    print("Job Not Found")
            else:
                print("Job Not Found")
                self.iserror = True
                
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
