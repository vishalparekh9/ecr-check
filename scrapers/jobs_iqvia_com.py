import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOB_BOARD_IQVIA_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobs.iqvia.com/'

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
        self.domain = 'jobs.iqvia.com'
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
                url = f'https://jobs.iqvia.com/search-jobs/results?ActiveFacetID=6252001&CurrentPage={page}&RecordsPerPage=12&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters[0].ID=6252001&FacetFilters[0].FacetType=2&FacetFilters[0].Count=171&FacetFilters[0].Display=United+States&FacetFilters[0].IsApplied=true&FacetFilters[0].FieldName=&FacetFilters[1].ID=76671&FacetFilters[1].FacetType=1&FacetFilters[1].Count=86&FacetFilters[1].Display=Clinical+Data+Management&FacetFilters[1].IsApplied=true&FacetFilters[1].FieldName=&FacetFilters[2].ID=76672&FacetFilters[2].FacetType=1&FacetFilters[2].Count=317&FacetFilters[2].Display=Clinical+Operations&FacetFilters[2].IsApplied=true&FacetFilters[2].FieldName=&FacetFilters[3].ID=76673&FacetFilters[3].FacetType=1&FacetFilters[3].Count=153&FacetFilters[3].Display=Clinical+Project+Management/Leadership&FacetFilters[3].IsApplied=true&FacetFilters[3].FieldName=&FacetFilters[4].ID=76686&FacetFilters[4].FacetType=1&FacetFilters[4].Count=244&FacetFilters[4].Display=Monitoring&FacetFilters[4].IsApplied=true&FacetFilters[4].FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=5&SortDirection=1&SearchType=6&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
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
                                    url = "https://jobs.iqvia.com" + link.find("a").get("href")
                                    jobObj['url'] = url
                                    jobObj['title'] = link.find("h2").text.strip()
                                    jobObj["location"] = link.find("span", {"class": "job-location"}).text.strip()
                                    isloaded, res = self.get_request(url)
                                    if isloaded:
                                        jobDetails = BeautifulSoup(res.text, "lxml")
                                        desc = str(jobDetails.find("section", {"class": "job-description"}))
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
