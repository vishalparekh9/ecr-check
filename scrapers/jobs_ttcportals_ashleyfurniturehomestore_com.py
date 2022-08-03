
import json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOBS_BRT_MV_ASHLEYFURNITUREHOMESTORE'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.ashleyfurniturehomestore.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'Content-Type': 'application/json'
        }

        self.session = requests.session()
        self.domain = 'ashleyfurniturehomestore.com'
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
                url = f'https://ashleycareers.ttcportals.com/search/jobs/in?cfm4%5B%5D=IT&cfm4%5B%5D=MARKETING&cfm4%5B%5D=ENGINEERING&cfm4%5B%5D=QUALITY&ns_category=technology&page={page}#'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    links = data.find_all("div", {"class": "jobs-section__item padded-small"})
                    if len(links) > 0:
                        for rd in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = rd.find("a").text
                            jobObj['location'] = rd.find("div", {"class": "jobs-section__item-location"}).text.replace("\n", "").replace("\r", "").replace("	", "").replace("  ", "").strip()
                            url = "" + rd.find("a").get("href")
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                try:
                                    jobData = BeautifulSoup(jobres.text, "lxml")
                                    jd = jobData.find('div', {'class': 'columns large-11'})
                                    jobObj['description'] = str(jd)
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                                except Exception as e:
                                    print(e)
                                    pass
                    else:
                        print("Job Not Found")
                        break
    
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))