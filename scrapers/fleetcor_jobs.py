import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj

# Token
token = 'FLEET_COR_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://us61e2.dayforcehcm.com/CandidatePortal/en-US/fleetcor?'

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
        self.domain = 'fleetcor.com'
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
                print("Collecting page"+ str(page))
                isloaded, res = self.get_request(
                    f'https://us61e2.dayforcehcm.com/CandidatePortal/en-US/fleetcor?page={page}')
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    # print(data)
                    jobDataChunk = data.find('ul', {'class': 'search-results'})
                    if jobDataChunk:
                        titleDiv = jobDataChunk.find_all('div', {'class': 'posting-title'})
                        for postTitle in titleDiv:
                            jobObj = deepcopy(self.obj)
                            try:
                                aTag = postTitle.find('a')
                                token = aTag.get('href')
                                url = 'https://us61e2.dayforcehcm.com' + str(token)
                                jobObj['url'] = url
                                isloaded, resJobData = self.get_request(url)
                                if isloaded:
                                    jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                                    jobObj['title'] = str(jobDetails.find('h1').text.strip())
                                    jobObj['location'] = str(
                                        jobDetails.find('span', {'class': 'job-location'}).text.strip())
                                    jobObj['description'] = str(
                                        jobDetails.find_all('div', {'class': 'job-posting-section'})[1])
                            except:
                                pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                    else:
                        print('No Job Data Found!')
                        isPage = False

            else:
                isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))