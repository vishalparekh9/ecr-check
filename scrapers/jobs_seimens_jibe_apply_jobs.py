import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json
from index import get_obj

# Token
token = 'SIEMENS_JOBS_JIBE_APPLY'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobs.siemens.com/api/jobs?sortBy=relevance&page=2&brand=Smart%20Infrastructure&keywords=%22building%20robotics%22&internal=false&userId=ab625a11-67c2-4209-b32d-4bec09b1291e&sessionId=1031e858-5733-40ed-88f2-87f652f9d499&deviceId=3018857288&domain=siemensglobal.jibeapply.com'

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
        self.domain = 'siemens.com'
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
                url = f'https://jobs.siemens.com/api/jobs?sortBy=relevance&page={page}&brand=Smart%20Infrastructure&keywords=%22building%20robotics%22&internal=false&userId=ab625a11-67c2-4209-b32d-4bec09b1291e&sessionId=1031e858-5733-40ed-88f2-87f652f9d499&deviceId=3018857288&domain=siemensglobal.jibeapply.com'
                print(url)
                print("Collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    page = page + 1
                    if 'jobs' in res.json():
                        lis = res.json()['jobs']
                        if len(lis) == 0:
                            isdata = False
                            break
                        for link in lis:
                            a = link['data']['meta_data']['canonical_url']
                            if a is None:
                                isdata = False
                                break
                            jobObj = deepcopy(self.obj)
                            url = f'https://jobs.siemens.com/jobs/{link["data"]["slug"]}?lang=en-us&previousLocale=en-US'
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
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
