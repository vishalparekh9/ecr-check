from pydoc import isdata
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

# Token
token = 'VICTRA_ADP'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://recruiting.adp.com/srccar/public/RTI.home?c=1157551&d=ExternalCareerSite&grp=%22Sales-Direct%20B2B%22'

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
        self.domain = 'victra.com'
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

    def post_request(self, page):
        try:
            url = 'https://recruiting.adp.com/srccar/public/rest/1/1242951/search/'
            data = '{"filters":[{"name":"state","label":"State"},{"name":"city","label":"City"},{"name":"grp","label":"Job Category"},{"name":"typeOfFulltime","label":"Full-Time/Part-Time"},{"name":"zzregTemp","label":"Regular/Temporary"}],"results":{"pageTitle":"Search Results","zeroResultsMessage":"We\'re sorry but we have no job openings at this time that match your search criteria. Please try another search.","searchFailureMessage":"Oops! Something went wrong.  Search has encountered a problem. Try searching again","resultsFoundLabel":"results found","bookmarkText":"Bookmark This","pageSize":"100","sortOrder":"00001000","shareText":"Share","fields":[{"name":"ptitle","label":"Published Job Title"},{"name":"grp","label":"Functional Group"}]},"pagefilter":{"grp":["Sales-Direct B2B"],"page":'+str(page)+'},"rl":"enUS"}'
            res = self.session.post(url, headers=self.postHeaders, data=data)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                page = 1
                isdata = True
                while isdata:
                    print("collecting page: " + str(page))
                    isloaded, res = self.post_request(page)
                    page = page + 1
                    if isloaded and 'jobs' in res.json():
                        if len(res.json()['jobs']) == 0:
                            isdata = False
                        for link in res.json()['jobs']:
                            jobObj = deepcopy(self.obj)
                            url = 'https://recruiting.adp.com/srccar/public/rest/1/1242951/job/' + link['id']
                            jobObj['url'] = link['url']
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                jobObj['title'] = link['ptitle']
                                jobObj['location'] = link['city'] + ', ' + link['state']
                                for js in jobres.json()['fields']:
                                    jobObj['description'] += js['content']

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
    print(scraper.allJobs)