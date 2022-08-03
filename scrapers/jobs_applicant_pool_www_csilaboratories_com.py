import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

# Token
token = 'JOBS_APPLICANT_POOL_WWW_CSILABORATRIES'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://csilaboratories.applicantpool.com/jobs/?linkId=hd.more.career'

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
        self.domain = 'csilaboratories.com'
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
                aTag = data.find_all('a', {'class': 'list-group-item strip-side-borders'})
                if aTag:
                    for link in aTag:
                        jobObj = deepcopy(self.obj)
                        url = link.get('href')
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        jobDetail = BeautifulSoup(jobres.text, 'lxml')
                        if isloaded:
                            jobDetail = BeautifulSoup(jobres.text, 'lxml')
                            jobObj['title'] = jobDetail.find('h1').text.strip()

                            jobObj['location'] = jobDetail.find('b', {'title': 'Location'}).parent.parent.text.strip()

                            regex = re.compile('.*row text-left.*')
                            descs = jobDetail.find('div', {'class': regex}).find('div', {'class': 'col-sm-7'}).find(
                                'hr')
                            jobObj['description'] += str(descs.find_next_siblings('div'))
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
