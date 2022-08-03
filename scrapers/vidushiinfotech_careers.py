import re
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'KEKAHIRE_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://vidushiinfotech.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'vidushiinfotech.com'
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
            url = f'https://vidushi.kekahire.com/api/jobs/active'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('jobpost')
                if len(links) > 0:
                    for link in links:
                        if link.find('id') is not None:
                            jobObj = deepcopy(self.obj)
                            url = "https://vidushi.kekahire.com/jobdetails/" + link.find('id').text
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                try:
                                    jobDetail = BeautifulSoup(jobres.text, 'lxml')
                                    jobObj['title'] = link.find('title').text.replace('\n', '').replace('\r', '').strip()
                                    jobObj['location'] = link.find('d3p1:countrycode').text + " / " + link.find("d3p1:city").text.strip()
                                    jobObj['description'] = str(jobDetail.find('div', {'class': 'job-details-container mb-5'}))
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                                except:
                                    pass
                else:
                    print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
