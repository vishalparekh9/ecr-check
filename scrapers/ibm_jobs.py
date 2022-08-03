
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'IBM_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.ibm.com'

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
        self.domain = 'ibm.com'
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
            url = 'https://jobsapi-internal.m-cloud.io/api/stjobbulk?organization=2242&limitkey=4A8B5EF8-AA98-4A8B-907D-C21723FE4C6B&facet=publish_to_cws:true&facet=primary_country:US&fields=ref,title,primary_city,primary_state,primary_country,primary_category,level,url,sub_category,addtnl_locations,brand'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = res.json()['queryResult']
                if data:
                    for link in data:
                        try:
                            jobObj = deepcopy(self.obj)
                            url = str(link['url'])
                            jobObj['url'] = url
                            jobObj['title'] = link['title']
                            jobObj['location'] = str(link['primary_city'] + ", " + link['primary_state'])
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, 'lxml')
                                import json
                                jData = json.loads(str(data.find_all('script', {'type': 'application/ld+json'})[1].text))
                                jobDesc = jData['description']
                                jobObj['description'] = jobDesc
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                        except:
                            pass
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
