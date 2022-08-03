# "https://jobs.ebayinc.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf="
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import json
import re

# Token
token = 'CAREER_GOOGLE_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.google.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'google.com'
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
                print("Collecting for page " +  str(page))
                url = f'https://careers.google.com/api/v3/search/?location=United%20States&q=&page={page}'
                page = page + 1
                isloaded, res = self.get_request(url)
                if isloaded:
                    if 'jobs' not in res.json(): break
                    data = res.json()['jobs']
                    if data:
                        if data is not None and len(data) > 0:
                            for link in data:
                                jobObj = deepcopy(self.obj)
                                if link['id'] != "":
                                    jobObj['url'] = 'https://careers.google.com/jobs/results/'+str(link['id']).replace('jobs/','')
                                    jobObj['company'] = link['company_name']
                                    jobObj['title'] = link['title']
                                    try:
                                        jobObj['location'] = str(link['locations'][0]['display'])
                                    except:
                                        pass
                                    try:
                                        jobObj['description'] = str(link['description'])+ "<br />" 
                                        jobObj['description'] = jobObj['description'] + link['responsibilities'] + "<br />" 
                                        jobObj['description'] = jobObj['description'] + link['qualifications']
                                    except:
                                        pass
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj['title'])
                                        print(jobObj['url'])

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
