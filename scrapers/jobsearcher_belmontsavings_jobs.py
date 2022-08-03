import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
import re
#Token
token = 'JOBSEARCHER_BELMONTSAVINGS_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobsearcher.com/c/Belmont%20Savings%20Bank' 

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
        self.domain = 'belmont-savings.com'
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
            page = 1
            isdata = True
            while isdata:
                print("collecting page " + str(page))
                isloaded, res = self.get_request(self.baseUrl + '?page=' + str(page))
                page = page + 1
                if isloaded:
                    regex1 = re.compile('.*widget__Widget-sc-lkaahn-0.*')
                    regex = re.compile('.*title__JobTitle-sc.*')
                    data = BeautifulSoup(res.text, 'lxml')
                    # print(data)
                    if data.find('section',{'class':regex1}):
                        links = data.find('section',{'class':regex1}).find_all('section',{'class':regex})
                    else:
                        isdata = False
                        break
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = 'https://jobsearcher.com' + link.find('a').get('href')
                            jobObj['url'] = url
                            isloaded, resJobData = self.get_request(url)
                            if isloaded:
                                jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                                regex = re.compile('.*ompany-and-location__LocationLink-sc-.*')
                                jobObj['title'] = jobDetails.find('h1').text.strip()
                                jobObj['location'] = jobDetails.find('a',{'class':regex}).text.strip()
                                regex = re.compile('.*bullets-styled__Wraper-sc-.*')
                                jobObj['description'] = str(jobDetails.find('div',{'class':regex}))
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj['title'])
                    else:
                        print('No Job Data Found!')
                        isdata = False
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))