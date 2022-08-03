import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj

# Token
token = 'COMCAST_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://comcast.com/'

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
        self.domain = 'comcast.com'
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
            isPage = True
            while isPage:
                page = page + 1
                print("Collecting page " + str(page))
                isloaded, res = self.get_request(f'https://comcast.jibeapply.com/api/jobs?location=united%20states&page={page}&sortBy=relevance&descending=false&internal=false&userId=6d85a220-a776-4584-9c50-3931d18ace7d&sessionId=6944dcbf-c042-45ac-8003-b5a990df1919&deviceId=3647768202&domain=comcast.jibeapply.com')
                if isloaded:
                    try:
                        data = res.json()['jobs']
                        if len(data) == 0:
                            break
                        for link in data:
                            if link is not None:
                                jobObj = deepcopy(self.obj)
                                url = str(link['data']['apply_url'])
                                jobObj['url'] = url
                                jobObj['title'] = str(link['data']['title'])
                                jobObj['location'] = str(link['data']['full_location'])
                                jobObj['description'] = str(link['data']['description'])
                                if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['description'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    except:
                        pass
                else:
                    isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))