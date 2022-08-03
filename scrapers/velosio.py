import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'VELOSIO'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'http://velosio.com/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'velosio.com'
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
            ispage = True
            while ispage:
                page = page + 1
                url = 'https://careers.velosio.com/api/jobs?page='+str(page)+'&sortBy=relevance&descending=false&internal=false&userId=ab6e4508-9e5a-4ab4-987e-6a43fe121f3b&sessionId=5e7e4fa8-a2a9-48fa-ae13-cca9954c7ceb&deviceId=1036133625&domain=velosio.jibeapply.com'
                print()
                print(url)
                print()
                isloaded, res = self.get_request(url)
                if isloaded:
                    links = res.json()['jobs']
                    print(len(links))
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = str(link['data']['title'])
                            jobObj['location'] = str(link['data']['country'])
                            jobObj['description'] = str(link['data']['description'])
                            jobObj['url'] = str(link['data']['apply_url'])
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                    else:
                        ispage = False
                        break
                else:
                    print("Job Not Found")
            else:
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)