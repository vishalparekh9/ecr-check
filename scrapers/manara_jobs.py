import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'MANARA_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://manara.tech/careers' 

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
        self.domain = 'manara.tech'
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
            regex = re.compile('.*https://manara.tech/_next/static/chunks/pages/careers-.*')
            # descs = jobDetail.find_all('div',{'class':regex})
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('script',{'class':'pt-6'})
                if links:
                    for link in links:
                        print(data.find_all('a',{'class':'btn-orange-filled'}))
                        break
                        jobObj = deepcopy(self.obj)
                        try:
                            url = link.find('a',{'class':'btn-orange-filled'}).get('href')
                            jobObj['url'] = url
                            jobObj['title'] = link.find('span',{'class':'text-2xl font-semibold'}).text.strip()
                            jobObj['location'] = 'united states'
                            jobObj['description'] = str(link.find('p',{'class':'mb-6 text-lg'}))
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                        except:
                            pass
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