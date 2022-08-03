
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'HNMSYSTEMS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.hnmsystems.com/'

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
        self.domain = 'hnmsystems.com'
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
            url = 'https://public-rest33.bullhornstaffing.com/rest-services/1D1609/query/JobBoardPost?where=(isOpen=true)&fields=id,title,publishedCategory(id,name),address(city,state),employmentType,dateLastPublished,publicDescription,isOpen,isPublic,isDeleted&count=1000&orderBy=-dateLastPublished&start=0'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = res.json()["data"]
                if data:
                    for link in data:
                        jobObj = deepcopy(self.obj)
                        jobObj['title'] = link['title'].replace("\r", "").replace("\n", "").strip()
                        Ids = link['id']
                        url = "https://www.hnmsystems.com/openjobs/#/jobs/"+str(Ids)+""
                        jobObj['url'] = url

                        city = str(link['address']['city']).replace("None", '')
                        state = str(link['address']['state']).replace("None", '')

                        if city is not None:
                            city = city.strip()

                        if state is not None:
                            state = state.strip()

                        jobObj['location'] = str(city) + " . " + str(state)
                        jobObj['description'] = str(link['publicDescription'])
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))




