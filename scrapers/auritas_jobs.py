import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'AURISTAS_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.auritas.com/careers/' 

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
        self.domain = 'auritas.com'
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
            # regex = re.compile('.*job-desc-block.*')
            # descs = jobDetail.find_all('div',{'class':regex})
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('h2',{'class':'elementor-heading-title elementor-size-default'})
                if links:
                    for link in links:
                        if link.find('a') == None: continue
                        url = link.find('a').get('href')
                        jobObj = deepcopy(self.obj)
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            try:
                                jobObj['title'] = jobDetail.find('h1',{'class':'elementor-heading-title elementor-size-default'}).text.strip()
                                jobObj['location'] = jobDetail.find(text='LOCATION').parent.parent.parent.parent.find_next_sibling('div').text.strip()
                                jobObj['description'] = str(jobDetail.find(text='WHAT YOU WILL DO').parent.parent.parent.parent)
                            except:
                                pass
                            if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['location'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['location'])
                                print(jobObj['title'])
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))