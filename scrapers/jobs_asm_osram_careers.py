import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'AMS_OSRAM_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.ams.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'ams.com'
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
            page = -15
            isPage = True
            while isPage:
                page = page + 15
                print("Collecting for page ", page)
                url = f'https://jobs.ams-osram.com/api/jobs/?start={page}&sortBy=date&sortOrder=desc&responseLanguage=en'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = res.json()['data']['jobs']
                    if len(data) > 0:
                        for link in data:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = link['title']
                            url = str('https://jobs.ams-osram.com/en/' + link['slug'])
                            jobObj['url'] = url
                            jobObj['location'] = link['country'] + ", " + link['state'] + ", " + link['city']
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                jobData = BeautifulSoup(res.text, "lxml")
                                jobDesc = jobData.find("div", {"class": "col-12 col-lg-7 col-xl-8 col-print-12"})
                                jobObj['description'] = str(jobDesc)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)

                    else:
                        print("Job Not Found")
                        isPage = False
            else:
                print("Job Not Found")
                isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)
