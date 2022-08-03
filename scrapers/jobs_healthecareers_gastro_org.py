
import json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOBS_HEALTH_E_CAREERS_GASTRO'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.gastro.org'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'gastro.org'
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
                url = f'https://www.healthecareers.com/aga/search-jobs/?catid=&pg={page}'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    link = data.find_all("div", {"class": "panel-container"})
                    if len(link) > 0:
                        for rd in link:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = rd.find("a", {"class": "job-title gtm-card-position"}).text
                            jobObj['location'] = str(rd.find("a", {"class": "job-title gtm-card-position"}).get('data-location'))
                            url = str(rd.find("a", {"id": "job-results-job-title"}).get("href"))
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                try:
                                    jobData = BeautifulSoup(jobres.text, "lxml")
                                    jd = jobData.find('div', {'class': 'description inner-html-default'})
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