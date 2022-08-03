import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = '1STUNITEDCU_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://1stuscu.hrmdirect.com/employment/job-openings.php?search=true&nohd' 

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
        self.domain = '1stunitedcu.org'
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
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                regex = re.compile('.*ReqRowClick ReqRowClick.*')
                trs = data.find_all('tr',{'class':regex})
                if trs:
                    for link in trs:
                        jobObj = deepcopy(self.obj)
                        url = 'https://1stuscu.hrmdirect.com/employment/' + link.find('a').get('href')
                        jobObj['url'] =  url
                        isloaded, jobres = self.get_request(url)
                        jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                        if isloaded:
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            jobObj['title'] = jobDetail.find('h2').text.strip()
                            jobObj['location'] = link.find_all('td')[3].text.strip() + ', ' +link.find_all('td')[4].text.strip()
                            jobObj['description'] = str(jobDetail.find('div',{'class':'jobDesc'}))
                            
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))