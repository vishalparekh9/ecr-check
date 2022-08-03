
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOBS_PGE_CAREERS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://pge.com'

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
        self.domain = 'pge.com'
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
                url = f'https://jobs.pge.com/search-jobs/results?ActiveFacetID=0&CurrentPage={page}&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Banner+-+Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
                isloaded, res = self.get_request(url)
                if isloaded:
                    if len(res.json()['results']) > 1865:
                        jsonData = str(res.json()['results']).replace("\\'", "'").replace('\\"', '"').replace("\\n", "").replace("\\/", "/").strip()
                        data = BeautifulSoup(str(jsonData), 'lxml')
                        links = data.find_all('li')
                        if links:
                            for link in links:
                                jobObj = deepcopy(self.obj)
                                url = 'https://jobs.pge.com' + str(link.find("a").get('href'))
                                jobObj['url'] = url
                                if link.find('h2') is not None:
                                    try:
                                        jobObj['title'] = link.find('h2').text.replace("\r", "").replace("\n", "").strip()
                                        jobObj['location'] = link.find('span').text.replace("\r", "").replace("\n", "").strip()
                                        isloaded, res = self.get_request(url)
                                        if isloaded:
                                            jobData = BeautifulSoup(res.text, 'lxml')
                                            jobDesc = str(jobData.find('div', {'class': 'ats-description'}))
                                            jobObj['description'] = jobDesc
                                            if jobObj['title'] != '' and jobObj['url'] != '':
                                                self.allJobs.append(jobObj)
                                                print(jobObj)
                                    except (Exception, AttributeError, KeyError, ValueError) as e:
                                        pass
                                else:
                                    isPage = False
                                    break
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
    print(scraper.allJobs)