# "https://jobs.ebayinc.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf="
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import json
import re

# Token
token = 'EBAY_INC_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.ebayinc.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'referer': 'https://www.careerbuilder.com/jobs?country_code=US&keywords=DATA+ANALYST',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.session = requests.session()
        self.domain = 'ebayinc.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def get_request(self, url):
        try:
            res = self.session.get(url, headers=self.getHeaders)
            print("here")
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
                url = f'https://jobs.ebayinc.com/search-jobs/results?ActiveFacetID=0&CurrentPage={page}&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    import json
                    htmlData2 = str(json.loads(res.text)['results'])
                    data = BeautifulSoup(htmlData2, "lxml")
                    if data:
                        links = data.find("section", {"id": "search-results-list"}).find_all("li")
                        if links is not None and len(links) > 0:
                            for link in links:
                                jobObj = deepcopy(self.obj)
                                try:
                                    if link.find("a").get("href") != "":
                                        jobObj['title'] = link.find("h2").text
                                        url = str("https://jobs.ebayinc.com" + link.find("a").get("href"))
                                        jobObj['url'] = url
                                        jobObj['location'] = str(link.find("span", {"class": "job-location"}).text)
                                        isloaded, res = self.get_request(url)
                                        if isloaded:
                                            jobData = BeautifulSoup(res.text, "lxml")
                                            jobDesc = jobData.find("div", {"class": "ats-description"})
                                            jobObj['description'] = str(jobDesc)
                                            if jobObj['title'] != '' and jobObj['url'] != '':
                                                self.allJobs.append(jobObj)
                                                print(jobObj)
                                except:
                                    pass

                        else:
                            print("Job Not Found")
                            ispage = False
                            break
                    else:
                        print("Job Not Found")
                        ispage = False
                        break
            else:
                print("Job Not Found")
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)
