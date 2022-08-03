import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
import re
#Token
token = 'HRMDIRECT_CAROTEK_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.host= 'https://sunsrce.hrmdirect.com'
        self.baseUrl = self.host + '/employment/job-openings.php?search=true' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        self.session = requests.session()
        self.domain = 'carotek.com'
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
            print(self.baseUrl)
            if isloaded:
                regex = re.compile('.*job-opening.php\?req=.*')
                soup = BeautifulSoup(res.text, 'lxml')
                links = soup.find_all('a',{'href':regex})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = self.host + '/employment/' +link.get('href')
                        jobObj['url'] = url
                        isloaded, resJobData = self.get_request(url)
                        if isloaded:
                            soup = BeautifulSoup(resJobData.text, 'lxml')
                            try:
                                jobObj['title'] = soup.find('h2').text.strip()
                                try:
                                    for loc in soup.find('table',{'class':'viewFields'}).find_all('tr'):
                                        if 'location' in loc.text.strip().lower():
                                            jobObj['location'] = loc.text.strip().replace('Location:','').strip()
                                except:
                                    pass
                                jobObj['description'] = soup.find('div',{'class':'jobDesc'}).text.strip()
                            except:
                                pass
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
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