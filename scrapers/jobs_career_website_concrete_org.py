
import json
import re

import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOBS_CAREER_WEBSITE_CONCRETE'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.concrete.org'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'concrete.org'
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
            while isPage:
                page = page + 1
                print("Collecting for page ", page)
                url = f'https://concrete.careerwebsite.com/c/@search_results/controller/includes/search_jobs.cfm?page={page}&pos_flt=0&location_autocomplete=true&radius=320&ajaxRequest=1'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    jdata = res.json()['search_results']
                    data = jdata.replace("\'", "'").replace('\"', '"').replace("\n", "").replace("\/", "/").replace("\t", "").strip()
                    links = BeautifulSoup(str(data).replace("\r", "").replace("\n", "").replace("	", ""), "lxml")

                    id = re.compile("job-tile-(.*?)job-tile status-highlight-vert")
                    jlinks = links.find_all("div", {"class": id})
                    if len(jlinks) > 0:
                        for rd in jlinks:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = rd.find("a").text
                            jobObj['location'] = rd.find("div", {"class": "job-location"}).text
                            url = "https://concrete.careerwebsite.com" + rd.find("a").get("href")
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                try:
                                    jobData = BeautifulSoup(jobres.text, "lxml")
                                    jd = jobData.find('div', {'class': 'job-main-desc'})
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

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))