import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'ZUUMAPP_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://zuumapp.com/careers/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.session = requests.session()
        self.domain = 'zuumapp.com'
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
            url = 'https://api.resumatorapi.com/v1/jobs/status/open?apikey=3UUp0T5lr7pwec716SHUkYNLjHwecuns'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = res.json()
                if len(data) > 0:
                    for link in data:
                        jobObj = deepcopy(self.obj)
                        jid = link['board_code']
                        url = f"https://zuum.applytojob.com/apply/{jid}]"
                        jobObj['url'] = url
                        jobObj['title'] = link['title']
                        jobObj['location'] = link['country_id'] + ", " + link['city']
                        jobObj['description'] = str(link['description'])
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)
                else:
                    print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))