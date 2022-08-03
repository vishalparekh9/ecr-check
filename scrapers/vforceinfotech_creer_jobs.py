import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'VFORCE_INFOTECH_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://vforceinfotech.com/'

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
        self.domain = 'vforceinfotech.com'
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
                isloaded, res = self.get_request(f'https://api.ceipal.com/7c2b04be9dd6e312548fa1dd5dde52bbd5b51fa7f706bcea04/job-postings/?page={page}')
                if isloaded:
                    data = res.json()['results']
                    for link in data:
                        if link is not None:
                            jobObj = deepcopy(self.obj)
                            url = str(link['apply_job_without_registration'])
                            jobObj['url'] = url
                            jobObj['title'] = str(link['position_title'])
                            jobObj['location'] = str(link['country'] + ", " + link['state'])
                            jobObj['description'] = str(link['public_job_desc'])
                            if jobObj['title'] != '' and jobObj['url'] != '' and len(jobObj['description']) > 255:
                                self.allJobs.append(jobObj)
                                print(jobObj)
                else:
                    isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))