import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import json
#Token
token = 'STRIP_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://stripe.com/jobs/search?office_locations=North+America--Chicago&office_locations=North+America--Mexico+City&office_locations=North+America--New+York&office_locations=North+America--Seattle&office_locations=North+America--South+San+Francisco&office_locations=North+America--Toronto' 

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
        self.domain = 'stripe.com'
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
            page = 0
            while True:
                isloaded, res = self.get_request(self.baseUrl + "&skip=" + str(page))
                print("collecting page" + str(page))
                page = page + 100
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('a',{'data-analytics-label':'jobs_listings_title_link'})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = 'https://stripe.com' + link.get('href')
                            try:
                                isloaded, jobres = self.get_request(url)
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                jobObj['url'] = url
                                jobObj['title'] = jobDetail.find('h1',{'class':'Copy__title'}).text.strip()
                                jobObj['location'] = link.parent.parent.find_all('td')[2].text.strip()
                                if isloaded:
                                    jobObj['description'] = str(jobDetail.find('div',{'class':'ArticleMarkdown'}))
                            except:
                                pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['title'])
                    else:
                        break
                        print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))