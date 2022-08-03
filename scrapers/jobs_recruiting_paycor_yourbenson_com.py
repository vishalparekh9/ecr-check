
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'JOBS_RECRUITING_PAYCOR_YOURBENSON_COM'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://recruitingbypaycor.com/career/CareerHome.action?clientId=8a788267574b28b701574ecf6d140298'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://recruitingbypaycor.com/career/',
            'clientId': '8a788267574b28b701574ecf6d140298',
            'parentUrl': 'https://recruitingbypaycor.com/career/',
            'gns': '',
        }
        self.session = requests.session()
        self.domain = 'yourbenson.com'
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
            url = 'https://recruitingbypaycor.com/career/CareerHome.action?clientId=8a788267574b28b701574ecf6d140298'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.findAll('li', {'class': 'gnewtonJobNode'})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = link.find('a').get('href')
                        print(url)
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            jobDetail = BeautifulSoup(jobres.text, 'lxml')
                            jobObj['title'] = link.find('a').text.strip()
                            jobObj['location'] = jobDetail.find('td', {'id': 'gnewtonJobLocationInfo'}).text.strip()
                            jobObj['description'] = str(jobDetail.find('table', {'id': 'gnewtonJobDescription'}))
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