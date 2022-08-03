import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'HITACHI_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://hitachi.com'

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
        self.domain = 'hitachi.com'
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
                url = f'https://careers.hitachi.com/search/jobs/in?location=&page={page}&q=#'
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('div', {"class": "jobs-section__item page-section-1"})
                    if links:
                        for link in links:
                            if link.find('div', {"class": "large-4 columns"}) is not None:
                                jobObj = deepcopy(self.obj)
                                url = str(link.find('a').get('href'))
                                jobObj['url'] = url
                                jobObj['title'] = link.find('a').text.replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "").strip()
                                jobObj['location'] = link.find('div', {"class": "large-4 columns"}).text.replace("\r", "").replace("  ", "").replace("\n", "").replace("\t", "").replace("Location: ", "").strip()
                                isloaded, res = self.get_request(url)
                                if isloaded:
                                    data = BeautifulSoup(res.text, 'lxml')
                                    jobDesc = str(data.find('div', {'class': 'page-section-2 space-2 job-description'}))
                                    jobObj['description'] = jobDesc
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                    else:
                        isPage = False
                        break
                else:
                    print("Job Not Found")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)