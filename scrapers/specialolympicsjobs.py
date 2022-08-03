import json
from pydoc import isdata
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'SPECIALOLYMPIC'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://recruiting.ultipro.com/SPE1016SPOL/JobBoard/48c569fb-e342-71d0-cf2c-f3622cec1d24/JobBoardView/LoadSearchResults' 

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
        self.domain = 'specialolympics.org'
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
            isdata = True
            while isdata:
                url = 'https://recruiting.ultipro.com/SPE1016SPOL/JobBoard/48c569fb-e342-71d0-cf2c-f3622cec1d24/JobBoardView/LoadSearchResults?Skip='+str(page)+'&Top=50'
                page = page + 50
                print("collecting records: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    links = res.json()['opportunities']
                    if len(links) > 0:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = 'https://recruiting.ultipro.com/SPE1016SPOL/JobBoard/48c569fb-e342-71d0-cf2c-f3622cec1d24/OpportunityDetail?opportunityId=' + str(link['Id'])
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            if isloaded:
                                jobObj['title'] = link['Title']
                                try:
                                    jobObj['location'] = link['Locations'][0]['Address']['City'] +', ' + link['Locations'][0]['Address']['State']['Code']
                                except:
                                    pass
                                try:
                                    if jobObj['location'] == '':
                                        jobObj['location'] = link['Locations'][1]['Address']['City'] +', ' + link['Locations'][1]['Address']['State']['Code']
                                except:
                                    pass
                                descs = jobDetail.find_all('script')
                                for desc in descs:
                                    try:
                                        if 'CandidateOpportunityDetail' in desc.text:
                                            des = desc.text.split('CandidateOpportunityDetail(')[1]
                                            des =des.split(');')[0]
                                            jsn = json.loads(des)
                                            jobObj['description'] = str(jsn['Description'])
                                    except:
                                        pass
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        print('No Job Data Found!')
                        isdata = False
                else:
                    isdata = False
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))