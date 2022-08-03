

import json
from copy import deepcopy
import time
import requests
from bs4 import BeautifulSoup
from index import get_obj

specialid = 'POW1005POGRE'
id = '4c470e1c-f1e3-4532-95a5-61c8a1d4d47e'
token = 'CEPOWER'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://recruiting.ultipro.com/' + str(specialid) + '/JobBoard/' + str(
            id) + '/JobBoardView/LoadSearchResults'

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
        self.domain = 'cepower.net'
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
            url = 'https://recruiting.ultipro.com/' + str(specialid) + '/JobBoard/' + str(
                id) + '/JobBoardView/LoadSearchResults?Skip=0&Top=50'

            isloaded, res = self.get_request(url)
            if isloaded:
                links = res.json()['totalCount']
                if int(links) > 0:

                    url = 'https://recruiting.ultipro.com/' + str(specialid) + '/JobBoard/' + str(
                        id) + '/JobBoardView/LoadSearchResults?Skip=0&Top=' + str(links) + ''

                    isloaded, res = self.get_request(url)
                    if isloaded:
                        links = res.json()['opportunities']
                        if len(links) > 0:
                            for link in links:
                                jobObj = deepcopy(self.obj)
                                url = 'https://recruiting.ultipro.com/' + str(specialid) + '/JobBoard/' + str(
                                    id) + '/OpportunityDetail?opportunityId=' + str(
                                    link['Id'])
                                jobObj['url'] = url
                                print(url)
                                time.sleep(5)

                                isloaded, jobres = self.get_request(url)

                                if jobres.text is not None:
                                    # print(jobres.text)
                                    jobDetail = BeautifulSoup(jobres.text, 'lxml')
                                    if isloaded:
                                        jobObj['title'] = link['Title']
                                        jobObj['location'] = link['Locations'][0]['Address']['City'] + ', ' + link['Locations'][0]['Address']['State']['Code']

                                        descs = jobDetail.find_all('script')
                                        for desc in descs:
                                            try:
                                                if 'CandidateOpportunityDetail' in desc.text:
                                                    des = desc.text.split('CandidateOpportunityDetail(')[1]
                                                    des = des.split(');')[0]
                                                    jsn = json.loads(des)
                                                    jobObj['description'] = str(jsn['Description'])
                                                    print(jobObj['description'])

                                            except:
                                                pass
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                    else:
                                        print('No Job Data Found!')
                                        isdata = False
                                else:
                                    print("desc not found")
            else:
                isdata = False
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))

            