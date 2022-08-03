import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'ZILLOW_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.adaptivebiotech.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'adaptivebiotech.com'
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
            page = -10
            isPage = True
            while isPage:
                page = page + 10
                print("Collecting for page ", page)
                url = f'https://career.zillowgroup.com/api/apply/v2/jobs?domain=zillowgroup.com&start={page}&num=10&pid=240528877353&domain=zillowgroup.com'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = res.json()
                    if len(data['positions']) > 0:
                        for rd in data['positions']:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = rd['name']
                            jobObj['location'] = str(rd['location'])
                            url = "https://career.zillowgroup.com/careers?pid=240528877353&domain=zillowgroup.com"
                            jobObj['url'] = url
                            jobObj['description'] = str(rd['job_description'])
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                    else:
                        print("No Jobs")
                        isPage = False
                        break
            else:
                print("Job Not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)
