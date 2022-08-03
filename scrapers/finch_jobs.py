import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'FINCH_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.finch.com/careers/' 

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }

        self.ajaxpostHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.session = requests.session()
        self.domain = 'finch.com'
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
    
    def post_request(self):
        try:
            url = 'https://www.finch.com/wp-admin/admin-ajax.php'
            params = {
                'filterdepts': 'Department',
                'filterlocs': 'Location',
                'action': 'myfilter'
            }
            res = self.session.post(url, headers=self.ajaxpostHeaders, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            regex = re.compile('.*https://www.finch.com/our-careers.*')
            # descs = jobDetail.find_all('div',{'class':regex})
            isloaded, res = self.post_request()
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('a',{'href':regex})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = link.get('href')
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            try:
                                jobObj['title'] = jobDetail.find('h1').text.strip()
                                jobObj['location'] = jobDetail.find('h1').find_next_sibling('p').text.strip().replace('Location:','').strip()
                                [x.extract() for x in jobDetail.findAll('h1')]
                                jobObj['description'] = str(jobDetail.find('div',{'class':'columns large-7 medium-12 small-12'}))
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