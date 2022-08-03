import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
import json
from index import get_obj

# Token
token = 'MY_WORKDAY_JOBS_CLIENT_ID_COSTARGROUP_COM'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://costar.wd1.myworkdayjobs.com/CoStarCareers?clientRequestID=328b70999939442fac502c1d55a1e027' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'application/json,application/xml',
            'X-Workday-Client': '2022.07.5',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.session = requests.session()
        self.domain = 'costargroup.com'
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
            jobtitles = []
            isdata = True
            page = 0
            while isdata:
                isdata = False
                url = 'https://costar.wd1.myworkdayjobs.com/CoStarCareers?clientRequestID=328b70999939442fac502c1d55a1e027'
                print("Collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    page = page + 50
                    if 'listItems' in res.json()['body']['children'][0]['children'][0]:
                        lis = res.json()['body']['children'][0]['children'][0]['listItems']
                        if len(lis) == 0:
                            isdata=False
                            break
                        for link in lis:
                            a = link['title']['commandLink']
                            if a == None:
                                isdata = False
                                break
                            jobObj = deepcopy(self.obj)
                            url = 'https://costar.wd1.myworkdayjobs.com' + a
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                try:
                                    if link['title']['instances'][0]['text'] not in jobtitles:
                                        jobtitles.append(link['title']['instances'][0]['text'])
                                        jobObj['title'] = link['title']['instances'][0]['text']
                                        jobObj['location'] = json.loads(jobres.json()['structuredDataAttributes']['data'])['jobLocation']['address']['addressLocality']
                                        jobObj['description'] = json.loads(jobres.json()['structuredDataAttributes']['data'])['description']
                                    else:
                                        isdata = False
                                        break
                                except Exception as e:
                                    print(e)
                                    pass
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)

                    else:
                        isdata = False
                        print('No Job Data Found!')
                else:
                    isdata = False
        except Exception as e:
            print(e)
            self.iserror = True
            isdata = False

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))