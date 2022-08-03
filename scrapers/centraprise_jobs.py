import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'CENTRAPRISE_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://centraprise.com/'

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
        self.domain = 'centraprise.com'
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
                print("collecting page " + str(page))
                isloaded, res = self.get_request(f'https://api.ceipal.com/cHhEc0psVEZNOEI5VkkvU1BjUHlIZz09/job-postings/?page={page}')
                if isloaded:
                    if 'results' not in res.json():
                        break
                    data = res.json()['results']
                    if len(data) == 0:
                        break
                    for link in data:
                        try:
                            if link is not None:
                                jobObj = deepcopy(self.obj)
                                try:
                                    url = str(link['apply_job_without_registration'])
                                    jobObj['url'] = url
                                    jobObj['title'] = str(link['position_title'])
                                    jobObj['location'] = str(link['country'] + ", " + link['state'])
                                    jobObj['description'] = str(link['public_job_desc'])
                                except Exception as e:
                                    print(e)
                                    pass
                                if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['description'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj['title'])
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