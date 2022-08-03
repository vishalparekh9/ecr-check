import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = '1AAUTO'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.1aauto.com/careers' 

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
        self.domain = '1aauto.com'
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
                links = data.find_all('a')
                if links:
                    for link in links:
                        try:
                            if '/mascsr/default/mdf/recruitment/recruitment.html?cid=' in link.get('href'):
                                jobObj = deepcopy(self.obj)
                                url = link.get('href')
                                jobObj['url'] = url
                                jobId = url.split('jobId=')[1]
                                jobId = jobId.split('&')[0]
                                url ='https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions/'+str(jobId) + '?cid=57042bca-f85f-4ab8-b594-cedc1ffdaa5f&lang=en_US&ccId=19000101_000001&locale=en_US'
                                isloaded, jobres = self.get_request(url)
                                if isloaded:
                                    if 'requisitionTitle' in jobres.json():
                                        jobDetail= jobres.json()
                                        jobObj['title'] = jobDetail['requisitionTitle']
                                        try:
                                            jobObj['location'] = jobDetail['requisitionLocations'][0]['nameCode']['shortName'].strip()
                                        except:
                                            pass
                                        jobObj['description'] = str(jobDetail['requisitionDescription'])
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                        except:
                            pass
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))