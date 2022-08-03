import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'FUSION180'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobs.deluxe.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=15&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=True&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf=' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Host': 'jobs.deluxe.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.session = requests.session()
        self.domain = '1800accountant.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
    def get_request(self, url):
        try:
            res = self.session.get(url)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            page = 1
            isdata = True
            while isdata:
                print("collecting page: "+ str(page))
                url = 'https://jobs.deluxe.com/search-jobs/results?ActiveFacetID=0&CurrentPage='+str(page)+'&RecordsPerPage=15&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=True&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
                page = page + 1
                isloaded, res = self.get_request(url)
                if isloaded and 'results' in res.json():
                    data = BeautifulSoup(res.json()['results'], 'lxml')
                    links = data.find_all('li')
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            try:
                                url = 'https://jobs.deluxe.com' + link.find('a').get('href')
                                jobObj['url'] = url
                                isloaded, jobres = self.get_request(url)
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                if isloaded:
                                    jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                    jobObj['title'] = jobDetail.find('h1').text.strip()
                                    jobObj['location'] = jobDetail.find('span',{'class':'job-location job-info'}).text.strip().replace('Location','').strip()
                                    jobObj['description'] = str(jobDetail.find('div',{'class':'ats-description'}))
                                    
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                            except:
                                pass
                    else:
                        isdata = False
                        print('No Job Data Found!')
                else:
                    isdata = False
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))