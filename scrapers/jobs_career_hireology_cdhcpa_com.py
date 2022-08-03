
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'JOBS_CAREERS_HIREOLOGY_CDHCPA'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.hireology.com/cdh'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'cdhcpa.com'
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
                url = f'https://api.hireology.com/v2/public/careers/cdh?ref=career_site&ref_m=application&widget=t&xdm_c=default9161&xdm_e=https://sites.hireology.com&xdm_p=1&sort=jobs.created_at&sort_dir=desc&page={page}&page_size=10'
                isloaded, res = self.get_request(url)
                if isloaded:
                    links = res.json()['data']
                    if len(links) > 0:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = str(link['career_site_url'])
                            jobObj['url'] = url
                            jobObj['title'] = link['name']
                            jobObj['location'] = link['locations'][0]['city'] + ", " + link['locations'][0]['state']
                            jobObj['description'] = link['job_description']
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                    else:
                        isPage = False
                        print("Job Not Found")
                        break
                else:
                    print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
