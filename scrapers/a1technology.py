import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
#Token
token = 'A1TECHNOLOGY'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.a1technology.com/careers.aspx' 

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
        self.domain = 'www.a1technology.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
    def get_request(self, url):
        try:
            res = self.session.get(url, headers=self.getHeaders, timeout=10)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
#                 print(data)
                jobDataChunk = data.find('table')
                if jobDataChunk:
                    jobObj = deepcopy(self.obj)
                    trs = jobDataChunk.find_all('tr')
                    for tr in trs:
                        tds = tr.find_all('td')
                        if tds == []:
                            pass
                        else:
                            id = tds[0].text.strip()

                            jobUrl = 'https://www.a1technology.com/JobDetail.aspx?IdPassed=' + str(id)
                            jobObj['url'] = jobUrl
                            
                            isloaded, resData = self.get_request(jobUrl)
                            if isloaded:
                                jobData = BeautifulSoup(resData.text, 'lxml')
                                jobObj['title'] = jobData.find('span',{'id':'ctl00_ContentPlaceHolder1_lblPosition'}).text
                                jobObj['description'] = jobData.find('span',{'id':'ctl00_ContentPlaceHolder1_lblJobDescription'}).text
                                jobObj['location'] = jobData.find('span',{'id':'ctl00_ContentPlaceHolder1_lblCountry'}).text

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