import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj

# Token
token = 'CAPGEMINI_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://capgemini.com/'

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
        self.domain = 'capgemini.com'
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
                print("collecting pages " + str(page))
                isloaded, res = self.get_request(f'https://www.capgemini.com/us-en/careers/job-search/page/{page}/?show_posts=100')
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('div', {'class': 'section__block col-12'})
                    if len(links) == 0:
                        break
                    islinks = False
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = '' + str(link.find("a").get("href"))
                        islinks = True
                        jobObj['url'] = url
                        try:
                            jobObj['title'] = str(link.find('a').text.strip())
                            jobObj['location'] = str(link.find('span').text.strip())
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                jobDetails = BeautifulSoup(res.text, 'lxml')
                                jobObj['description'] = str(jobDetails.find('div', {'class': 'article-text'}))
                        except:
                            pass
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj['title'])
                        if islinks == False:
                            break
                else:
                    isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))