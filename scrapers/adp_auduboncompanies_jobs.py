import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'ADP_AUDUBONCOMPANIES_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://recruiting.adp.com/srccar/public/RTI.home?d=AudubonCareers&_icx=v02xIB76Se6kk3bg5xvWg8zbMB8i__FyeUsmx6T4lQel3xGIMvaVWJFJubjRnXxNh22&c=1129507&_dissimuloSSO=UALcyCd0Z2Y:Av7vl08geZWWvvCqIl2neNEnLXM' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.postHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8'
        }
        self.session = requests.session()
        self.domain = 'auduboncompanies.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
        self.csid = ''
    def get_request(self, url):
        try:
            res = self.session.get(url, headers=self.getHeaders)
            return True, res
        except Exception as e:
            print(e)
        return False, False
    
    def post_request(self, page):
        try:
            url = 'https://recruiting.adp.com/srccar/public/rest/1/'+str(self.csid)+'/search/'
            data = '{"filters":[{"name":"state","label":"State"},{"name":"city","label":"City"},{"name":"departmentCode","label":"Department"}],"results":{"pageTitle":"Search Results","zeroResultsMessage":"We re sorry but we have no job openings at this time that match your search criteria. Please try another search.","searchFailureMessage":"Oops! Something went wrong.  Search has encountered a problem. Try searching again","resultsFoundLabel":"Results Found. To sign up for job alerts for this search, be sure to click notify me in the navigation. To filter your results, click on narrow your results on the sidebar.","bookmarkText":"Bookmark This","pageSize":"250","sortOrder":"00001000","shareText":"Share","fields":[{"name":"ptitle","label":"Published Job Title"},{"name":"departmentCode","label":"Department"},{"name":"timestampStatusActive","label":"Date Active"}]},"pagefilter":{"page":'+str(page)+'},"rl":"enUS"}'
            res = self.session.post(url, headers=self.postHeaders, data=data)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                self.csid = res.text.split('csID=')[1]
                self.csid = self.csid.split(';')[0]
                page = 1
                isdata = True
                while isdata:
                    print("collecting page: " + str(page))
                    isloaded, res = self.post_request(page)
                    page = page + 1
                    if isloaded and 'jobs' in res.json():
                        if len(res.json()['jobs']) == 0:
                            isdata = False
                        print(res.json()['totalCount'])
                        for link in res.json()['jobs']:
                            jobObj = deepcopy(self.obj)
                            url = 'https://recruiting.adp.com/srccar/public/rest/1/'+str(self.csid)+'/job/'+link['id']
                            jobObj['url'] = link['url']
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                jobObj['title'] = link['ptitle']
                                jobObj['location'] = link['city'] + ', ' +link['state']
                                for js in jobres.json()['fields']:
                                    jobObj['description'] +=  js['content']
                                
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        print('No Job Data Found!')
                        isdata = False
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))