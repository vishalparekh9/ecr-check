import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
import json
from index import get_obj
#Token
token = 'ACCOLADE_CAREER'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.accolade.com/' 

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
        self.domain = 'careers.accolade.com'
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
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find('script',{'id':'__NEXT_DATA__'})
                if links:
                    jsn = json.loads(links.text)
                    for link in jsn['props']['pageProps']['extendedJobAds']:
                        jobObj = deepcopy(self.obj)
                        url = link['applyUrl']
                        try:
                            jobObj['url'] = url
                            jobObj['title'] = link['title']
                            jobObj['location'] = link['details']['location']['city'] + ',' +link['details']['location']['countryCode']
                            jobObj['description'] = link['jobAd']['companyDescription']['text']
                            jobObj['description'] += link['jobAd']['jobDescription']['text']
                            jobObj['description'] += link['jobAd']['qualifications']['text']
                            jobObj['description'] += link['jobAd']['additionalInformation']['text']
                        except:
                            pass
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