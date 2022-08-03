
import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj

# Token
token = 'JOBS_CAREER_JOBSCORE_INGENESIS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://ingenesis.com'

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
        self.domain = 'ingenesis.com'
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
            isloaded, res = self.get_request("https://careers.jobscore.com/careers/ingenesis/")
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                spanTag = data.find_all('span', {'class': 'js-job-title'})
                for link in spanTag:
                    jobObj = deepcopy(self.obj)
                    token = link.find('a').get('href')
                    url = 'https://careers.jobscore.com' + str(token)
                    jobObj['url'] = url
                    isloaded, resJobData = self.get_request(url)
                    if isloaded:
                        jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                        jobObj['title'] = str(jobDetails.find('h1', {'class': 'js-title'}).text.strip())
                        jobObj['location'] = str(
                            jobDetails.find('h2', {'class': 'js-subtitle'}).text.split('|')[1].strip())
                        jobObj['description'] = str(
                            jobDetails.find('div', {'class': 'js-area-container js-section-job-description'}))

                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)
            else:
                print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))