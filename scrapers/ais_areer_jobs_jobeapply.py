import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json
from index import get_obj

# Token
token = 'AIS_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.ais.com/api/jobs?page=2&sortBy=relevance&descending=false&internal=false&userId=a42b8189-2013-47e3-86c8-c546cb31cb66&sessionId=468320f7-e878-492e-b727-f3ec539d872c&deviceId=2469724523&domain=ais.jibeapply.com'

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
        self.domain = 'ais.com'
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
                url = 'https://careers.ais.com/api/jobs?page=' + str(
                    page) + '&sortBy=relevance&descending=false&internal=false&userId=a42b8189-2013-47e3-86c8-c546cb31cb66&sessionId=468320f7-e878-492e-b727-f3ec539d872c&deviceId=2469724523&domain=ais.jibeapply.com'
                print("Collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    page += 1
                    if 'jobs' in res.json():
                        lis = res.json()['jobs']
                        if len(lis) == 0:
                            isdata = False
                            break
                        for link in lis:
                            a = link['data']['apply_url']
                            if a is None:
                                isdata = False
                                break
                            jobObj = deepcopy(self.obj)
                            url = 'https://careers.ais.com/ais/jobs/' + str(
                                link['data']['slug']) + '?lang=en-us&previousLocale=en-US'
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            jobDetail = BeautifulSoup(jobres.text, 'lxml')
                            if isloaded:
                                try:
                                    jobObj['location'] = link['data']['full_location']
                                    jobObj['title'] = link['data']['title']
                                    jobDetail = BeautifulSoup(jobres.text, 'lxml')
                                    descs = jobDetail.find('script', {'type': 'application/ld+json'})
                                    desc = json.loads(descs.text)
                                    jobObj['description'] = desc['description']
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                                except:
                                    pass
                    else:
                        isdata = False
                        print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True
            isdata = False


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
