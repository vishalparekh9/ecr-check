# "https://jobs.ebayinc.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf="
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import json
import re

# Token
token = 'WALMART_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.walmart.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'referer': 'https://www.careerbuilder.com/jobs?country_code=US&keywords=DATA+ANALYST',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'walmart.com'
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
            page = 1
            isPage = True
            while isPage:
                page = page + 1
                print("Collecting for page ", page)
                url = f'https://careers.walmart.com/api/search?q=&page={page}&sort=rank&jobCategory=00000161-7bad-da32-a37b-fbef5e390000,00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-7bff-da32-a37b-fbffc8c10000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000&jobSubCategory=0000015a-a577-de75-a9ff-bdff284e0000&expand=department,brand,type,rate&jobCareerArea=all&type=jobs'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    if data:
                        links = data.find_all("li", {"class": "search-result job-listing"})
                        if links is not None and len(links) > 0:
                            for link in links:
                                jobObj = deepcopy(self.obj)
                                if link.find("a").get("href") != "":
                                    jobObj['title'] = link.find("a").text
                                    url = str("" + link.find("a").get("href"))
                                    jobObj['url'] = url
                                    jobObj['location'] = str(link.find("span", {"class": "job-listing__location"}).text)
                                    isloaded, res = self.get_request(url)
                                    if isloaded:
                                        jobData = BeautifulSoup(res.text, "lxml")
                                        jobDesc = jobData.find("section", {"class": "job-details"})
                                        jobObj['description'] = str(jobDesc)
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                            print(jobObj)

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
