import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOB_BOARD_BOSTON_SCIENTIFIC_COM_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://bostonscientific.com/'

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
        self.domain = 'bostonscientific.com'
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
            page = -25
            isPage = True
            while isPage:
                page = page + 25
                url = f'https://jobs.bostonscientific.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=US&startrow={page}'
                print(f"Collecting for row {page}")
                isloaded, res = self.get_request(url)
                if isloaded:
                    linksData = BeautifulSoup(res.text, "lxml")
                    links = linksData.find_all("tr", {"class": "data-row clickable"})
                    if len(links) > 2:
                        if links:
                            for link in links:
                                if link.find("a") is not None:
                                    jobObj = deepcopy(self.obj)
                                    url = "https://jobs.bostonscientific.com" + link.find("a").get("href")
                                    jobObj['url'] = url
                                    jobObj['title'] = link.find("td", {"class": "colTitle"}).text.strip().replace("\r", "").replace("\n", "").replace("Job            ", " - ")
                                    jobObj["location"] = link.find("span", {"class": "jobLocation"}).text.strip().replace("\r", "").replace("\n", "")
                                    isloaded, res = self.get_request(url)
                                    if isloaded:
                                        jobDetails = BeautifulSoup(res.text, "lxml")
                                        desc = str(jobDetails.find("div", {"class": "jobDisplay"}))
                                        jobObj['description'] = str(desc)
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                            print(jobObj)
                        else:
                            print("Job Not Found")
                    else:
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