import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOB_BOARD_TECHNOLOGIES_ATT_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://att.jobs/'

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
        self.domain = 'att.jobs'
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
                print(f"Collecting for page {page}")
                url = f'https://www.att.jobs/search-jobs/results?ActiveFacetID=0&CurrentPage={page}&RecordsPerPage=16&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=36864&FacetType=1&FacetFilters[0].ID=36864&FacetFilters[0].FacetType=1&FacetFilters[0].Count=1498&FacetFilters[0].Display=Technology&FacetFilters[0].IsApplied=true&FacetFilters[0].FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=2&OrganizationIds=117&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = res.json()['results']
                    if len(data) > 3000:
                        resData = data.replace("\\'", "'").replace('\\"', '"').replace("\\n", "").replace("\\/", "/").strip()
                        linksData = BeautifulSoup(resData, "lxml")
                        links = linksData.find_all("li")
                        if links:
                            for link in links:
                                if link.find("span", {"class": "job-location"}) is not None:
                                    jobObj = deepcopy(self.obj)
                                    url = "https://www.att.jobs" + link.find("a").get("href")
                                    jobObj['url'] = url
                                    jobObj['title'] = link.find("h2").text.strip()
                                    jobObj["location"] = link.find("span", {"class": "job-location"}).text.strip()
                                    isloaded, res = self.get_request(url)
                                    if isloaded:
                                        jobDetails = BeautifulSoup(res.text, "lxml")
                                        desc = str(jobDetails.find("div", {"class": "job-description"}))
                                        jobObj['description'] = str(desc)
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                            print(jobObj)
                    else:
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
