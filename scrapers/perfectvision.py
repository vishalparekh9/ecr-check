import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'PERFECT_VISION_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions?cid=f1e2c24b-9be5-46aa-8774-f656c6e9893d&timeStamp=1645443855260&lang=en_US&ccId=19000101_000001&locale=en_US&$top=50' 

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
        self.domain = 'perfect-vision.com'
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
                if 'jobRequisitions' in res.json():
                    for link in res.json()['jobRequisitions']:
                        try:
                            jobid = ''
                            for id in link['customFieldGroup']['stringFields']:
                                if id['nameCode']['codeValue'] == 'ExternalJobID':
                                    jobid = id['stringValue']
                            if jobid == '':
                                continue
                            jobObj = deepcopy(self.obj)
                            url ='https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions/'+str(jobid) + '?cid=f1e2c24b-9be5-46aa-8774-f656c6e9893d&timeStamp=1645444408525&lang=en_US&ccId=19000101_000001&locale=en_US'
                            jobObj['url'] = 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=f1e2c24b-9be5-46aa-8774-f656c6e9893d&ccId=19000101_000001&jobId='+str(jobid)+'&lang=en_US&source=LI'
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