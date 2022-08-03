import re
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'WELLBEATS_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://wellbeats.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'wellbeats.com'
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
            url = 'https://www.wellbeats.com/careers/'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.findAll('article', {'class': re.compile('elementor-post elementor-grid-item ecs-post-loop post-(.*?) job-openings type-job-openings status-publish format-standard hentry')})
                if links:
                    for link in links:
                        if link.find('a') is not None:
                            if "job-openings" in link.find('a').get('href'):
                                jobObj = deepcopy(self.obj)
                                url = "" + link.find('a').get('href')
                                jobObj['url'] = url
                                isloaded, jobres = self.get_request(url)
                                if isloaded:
                                    jobDetail = BeautifulSoup(jobres.text, 'lxml')
                                    jobObj['title'] = link.find('a').text.replace('\n', '').replace('\r', '').strip()
                                    jobObj['location'] = "United States"
                                    jobObj['description'] = str(jobDetail.find_all('div', {'class': 'elementor-widget-container'})[16])
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                else:
                    print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
