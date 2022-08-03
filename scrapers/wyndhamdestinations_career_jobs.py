import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'WYNDHAM_DESTINATIONS_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://wyndhamdestinations.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'wyndhamdestinations.com'
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
                url = f'https://careers.travelandleisureco.com/jobs/search?page={page}'
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    tbody = data.find("tbody")
                    links = tbody.findAll('tr')
                    if len(links) > 0:
                        for link in links:
                            if link.find('a') is not None:
                                jobObj = deepcopy(self.obj)
                                url = "" + link.find_all('td')[0].find('a').get('href')
                                jobObj['url'] = url
                                isloaded, jobres = self.get_request(url)
                                if isloaded:
                                    jobDetail = BeautifulSoup(jobres.text, 'lxml')
                                    jobObj['title'] = link.find_all('td')[0].text.replace('\n', '').replace('\r', '').strip()
                                    jobObj['location'] = link.find('td', {"class": "job-search-results-location"}).text.replace('\n', '').replace('\r', '').strip()
                                    jobObj['description'] = str(jobDetail.find('div', {'class': 'job-description'}))
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                    else:
                        print("Job not Found!")
                        isPage = False
                        break
                else:
                    print("Job not Found!")
                    isPage = False
            else:
                print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
