import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj

# Token
token = 'ABBTECH'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careerportal.abbtech.com/#/'

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
        self.domain = 'abbtech.com'
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
            jobid = ""
            url = 'https://public-rest32.bullhornstaffing.com/rest-services/2ORQCP/search/JobOrder?query=(isOpen:1)%20AND%20(isDeleted:0)&count=500&fields=id&sort=id'
            isloaded, res = self.get_request(url)
            if isloaded:
                for jobid in res.json()['data']:
                    url = 'https://careerportal.abbtech.com/#/jobs/'+str(jobid['id'])+''
                    print(url)

                    dataurl = 'https://public-rest32.bullhornstaffing.com/rest-services/2ORQCP/query/JobBoardPost?where=(id='+str(jobid['id'])+')&fields=id,title,publishedCategory(id,name),address(city,state,countryName),employmentType,dateLastPublished,publicDescription,isOpen,isPublic,isDeleted,publishedZip,salary,salaryUnit'
                    isloaded, res = self.get_request(dataurl)
                    if isloaded:
                        for data in res.json()['data']:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = str(url)
                            jobObj['title'] = data['title'].replace('\n', '').replace('\r', '').strip()
                            city = data['address']['city']
                            state = data['address']['state']
                            jobObj['location'] = str(city) + ', ' + str(state).replace('\n', '').replace('\r', '').strip()
                            jobObj['description'] = str(data['publicDescription'])

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
