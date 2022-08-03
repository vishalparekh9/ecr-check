from random import betavariate
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'GODADDY'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.godaddy.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=100&Distance=100&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf=' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.session = requests.session()
        self.domain = 'careers.godaddy.com'
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
            isdata = True
            page = 1
            while isdata:
                url = 'https://careers.godaddy.com/search-jobs/results?ActiveFacetID=0&CurrentPage='+str(page)+'&RecordsPerPage=100&Distance=100&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
                print("Collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    page = page + 1
                    if 'results' in res.json():   
                        data = BeautifulSoup(res.json()['results'], 'lxml')
                        lis = data.find_all('li')
                        if len(lis) == 0:
                            isdata = False
                            break
                        for link in lis:
                            a = link.find('a')
                            if a == None:
                                isdata = False
                                break
                            jobObj = deepcopy(self.obj)
                            url = 'https://careers.godaddy.com' + a.get('href')
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            if isloaded:
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                jobObj['title'] = jobDetail.find('h1').text.strip()
                                
                                jobObj['location'] = jobDetail.find_all('span',{'class','job-location'})[0].text.strip().replace('Primary Location:','').strip()
                                if (len(jobDetail.find_all('span',{'class','job-location'})) > 1):
                                    jobObj['location'] += ', ' + jobDetail.find_all('span',{'class','job-location'})[1].text.strip().replace('Additional location(s):','').strip()

                                regex = re.compile('.*iCIMS_InfoMsg.*')
                                descs = jobDetail.find('div',{'class':'ats-description'})
                                jobObj['description'] = str(descs)

                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))