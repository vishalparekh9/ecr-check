
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'TRIANZ_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.trianz.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'referer': 'https://careers.trianz.com/SearchJobs/SearchJobs',
        }
        self.session = requests.session()
        self.domain = 'trianz.com'
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
            url = 'https://careers.trianz.com/SearchJobs/SearchJobs'
            isloaded, res = self.get_request(url)
            url = 'https://careers.trianz.com/SearchJobs/BindSearchSkillData'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find_all("tr")
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        try:
                            url = str("https://careers.trianz.com" + link.find("td").get("href"))
                            if url is not None:
                                jobObj['url'] = url
                                jobObj['title'] = link.find("h3", {"class": "job_title_search"}).text.replace("\n", "").replace("\r", "").replace("Job Opening", "").strip()
                                jobObj['location'] = link.find('label', {"class": "job_title_location"}).text.replace("\n", "").replace("\r", "").strip()
                                isloaded, res = self.get_request(url)
                                if isloaded:
                                    data = BeautifulSoup(res.text, 'lxml')
                                    jobDesc = str(data.find('div', {'class': 'Jd_box_content'}))
                                    if jobDesc:
                                        jobObj['description'] = jobDesc
                        except:
                            pass
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))