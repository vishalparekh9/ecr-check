import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'ICIMSCAREER'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers-isc2.icims.com/jobs/search?ss=1' 

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
        self.domain = 'careers-isc2.icims.com'
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
                iframe = data.find('iframe',{'id':'noscript_icims_content_iframe'})
                if iframe:
                    url = iframe.get('src').replace('&amp;','&')
                    isloaded, res = self.get_request(url)
                    if isloaded == False:
                        self.iserror = True
                        return 
                data = BeautifulSoup(res.text, 'lxml')
                divs = data.find_all('div',{'class':'col-xs-12 title'})
                if divs:
                    for link in divs:
                        a = link.find('a')
                        jobObj = deepcopy(self.obj)
                        url = a.get('href')
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                        if isloaded:
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            jobObj['title'] = jobDetail.find('h1').text.strip()
                            
                            jobObj['location'] = jobDetail.find('div',{'class':'col-xs-6 header left'}).find_all('span')[1].text.strip()
                            
                            regex = re.compile('.*iCIMS_InfoMsg.*')
                            descs = jobDetail.find_all('div',{'class':regex})
                            h2s = jobDetail.find_all('h2',{'class':regex})
                            for (desc,h2) in [(desc,h2) for desc in descs for h2 in h2s]:
                                jobObj['description'] += str(h2)
                                jobObj['description'] += str(desc)
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