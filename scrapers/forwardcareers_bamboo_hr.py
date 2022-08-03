
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

token = 'FORWARD_CAREERS_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://forwardcareers.bamboohr.com/jobs/embed2.php?version=1.0.0'

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
        self.domain = 'goforward.com'
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
            url = 'https://forwardcareers.bamboohr.com/jobs/'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                text = data.find('script',{'id':'positionData'})
                if text:
                    import json
                    links = json.loads(text.contents[0])
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = 'https://forwardcareers.bamboohr.com/jobs/view.php?id=' + str(link['id']) + '&source=bamboohr'
                        jobObj['url'] = url
                        jobObj['title'] = link['jobOpeningName']
                        jobObj['location'] = link['location']['name']
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            jobDetail = BeautifulSoup(jobres.text, 'lxml')
                            jobObj['description'] = str(jobDetail.find('div', {'class': 'ResAts__card-content'}))

                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                else:
                    print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)