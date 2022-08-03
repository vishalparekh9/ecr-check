import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'GCBIJOBS_GLACIER_BANCORP'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.glacierbancorp.com/'

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
        self.domain = 'glacierbancorp.com'
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
                url = f'https://www.gbcijobs.com/api/jobs?location=United%20States&woe=12&stretchUnit=MILES&stretch=10&page={page}&sortBy=relevance&descending=false&internal=false&userId=e2aea439-42a8-4289-ab0e-1b4994470ea6&sessionId=ba3b642b-8085-4dbd-94ba-f0605b1d925f&deviceId=3647768202&domain=glacierbancorp.jibeapply.com'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    links = res.json()['jobs']
                    if len(links) > 0:
                        for link in links:
                            try:
                                jobObj = deepcopy(self.obj)
                                req_id = link['data']['req_id']
                                url = f"https://www.gbcijobs.com/jobs/{req_id}?lang=en-uss"
                                jobObj['title'] = link['data']['title']
                                jobObj['location'] = link['data']['city'] + ", " + link['data']['state'] + ", " + link['data']['country']
                                jobObj['url'] = url
                                jobObj['description'] = link['data']['description'] + " <br />" + link['data']['qualifications'] + " <br />" + link['data']['responsibilities']
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                            except (Exception, KeyError, AttributeError, ValueError) as e:
                                pass
                    else:
                        isPage = False
                else:
                    print("Job Not Found!")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))