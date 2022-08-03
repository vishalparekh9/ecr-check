import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

token = 'WURK_BREEZY_HR_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://wurk.breezy.hr/'

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
        self.domain = 'wurk.com'
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
            url = 'https://wurk.breezy.hr/'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find('div', {'class': 'positions-container'}).findAll('li', {'class': 'position transition'})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = str("https://wurk.breezy.hr") + str(link.find('a').get('href'))
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            jobDetail = BeautifulSoup(jobres.text, 'lxml')
                            jobObj['title'] = link.find('h2').text.replace('\n', '').replace('\r', '').strip()
                            jobObj['location'] = link.find('li', {'class': 'location'}).text.replace('\n', '').replace('\r', '').strip()
                            jobObj['description'] = str(jobDetail.find('div', {'class': 'description'}))

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
