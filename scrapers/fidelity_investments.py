
import json
from copy import deepcopy
import time
import requests
from bs4 import BeautifulSoup
from index import get_obj

token = 'FIDELITY_INVESTMENTS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobs.fidelity.com'

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
        self.domain = 'fidelity.com'
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
            ispage = True
            while ispage:
                print("collecting offset "+ str(page))
                url = 'https://jobsapi-google.m-cloud.io/api/job/search?callback=jobsCallback&pageSize=10&offset='+str(page)+'&companyName=companies%2F4cb35efb-34d3-4d80-9ed5-d03598bf1051&customAttributeFilter=(primary_country%3D%22US%22%20OR%20primary_country%3D%22UK%22%20OR%20primary_country%3D%22GB%22%20OR%20primary_country%3D%22DE%22%20OR%20primary_country%3D%22HK%22)%20AND%20(ats_portalid%3D%22Smashfly_22%22%20OR%20ats_portalid%3D%22Smashfly_36%22%20OR%20ats_portalid%3D%22Smashfly_38%22)%20AND%20country%3D%22US%22&orderBy=relevance%20desc'
                page = page + 10
                isloaded, res = self.get_request(url)
                if isloaded:
                    jsn = res.text + ";"

                    links = json.loads(jsn.replace("jobsCallback(",""). replace(");",""))['searchResults']
                    if len(links) == 0: break
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            try:
                                link = link['job']
                                jobObj['title'] = str(link['title'])
                                jobObj['location'] = str(link['primary_city'] + str(" - ") + link['primary_state'])
                                jobObj['description'] = str(link['description'])
                                jobObj['url'] = str(link['url'])
                            except:
                                pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['title'])
                    else:
                        isdata = False
                        break
            else:
                isdata = False
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))

