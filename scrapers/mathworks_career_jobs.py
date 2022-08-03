import re
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'MATHWORKS_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.mathworks.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'mathworks.com'
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
                url = f'https://www.mathworks.com/company/jobs/opportunities/search?page={page}'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    links = data.find("table", {"class": "table search_result_table"}).find_all("tr")
                    if len(links) > 0:
                        for rd in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = rd.find("a", {"id": re.compile("title_(.*?)")}).text
                            loc = rd.find("span", {"class": "add_font_color_tertiary"})
                            if loc is None:
                                jobObj['location'] = "United States"
                            else:
                                jobObj['location'] = loc.text
                            url = 'https://www.mathworks.com' + str(rd.find("a", {"id": re.compile("title_(.*?)")}).get("href"))
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                try:
                                    jobDetails = BeautifulSoup(jobres.text, "lxml")
                                    import json
                                    jsonJobDesc = json.loads(str(jobDetails.find("script", {"type": "application/ld+json"}).text))
                                    jobObj['description'] = str(jsonJobDesc['description'])
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                                except Exception as e:
                                    print(e)
                                    pass
                    else:
                        print("Job Not Found")
                        isPage = False
            else:
                print("Job Not Found")
                isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)