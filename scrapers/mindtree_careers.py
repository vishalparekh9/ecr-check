import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj

# Token
token = 'MINDTREE_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://mindtree.com/'

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
        self.domain = 'mindtree.com'
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
            page = -1
            isPage = True
            while isPage:
                page = page + 1
                print("collecting page" + str(page))
                isloaded, res = self.get_request(f'https://www.mindtree.com/careers/ajax-jobs-list?q=&jobIDs=&paragraph_entity_id=54776&specialization=&country=AMERICAS&city=&job_level=&page='+str(page)+'&keyword=')
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find('div', {'class': "job-results"}).find_all('li')
                    if len(links) == 0:
                        break
                    for link in links:
                        if link.find('h6') is not None:
                            jobObj = deepcopy(self.obj)
                            url = 'https://www.mindtree.com' + str(link.find("a").get("href")).strip()
                            jobObj['url'] = url
                            jobObj['title'] = str(link.find('h6').text.strip())
                            jobObj['location'] = str(link.find('p').text.strip())
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                jobDetails = BeautifulSoup(res.text, 'lxml')
                                jobObj['description'] = str(jobDetails.find('div', {'class': 'mt_career_job_des_wrapper'}))
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj['title'])
                            else:
                                print('No Job Data Found!')
                else:
                    isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))