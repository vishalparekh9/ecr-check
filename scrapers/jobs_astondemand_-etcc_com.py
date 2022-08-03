
import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj

# Token
token = 'JOBS_ATSONDEMAND_ETCC'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://etcc.atsondemand.com'
        self.session = requests.session()
        self.domain = 'cerecore.net'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def post_request(self, url):
        try:
            getHeaders = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'cid': '512657',
                'Content-Type': 'application/json;charset=UTF-8'
            }

            payload = "{---    \"keywords\": null,---    \"workLocations\": [],---    \"categories\": [],---    \"workTypes\": [],---    \"multiSegment\": false,---    \"latitude\": null,---    \"longitude\": null,---    \"radius\": null,---    \"locationBounds\": null,---    \"countryIso2\": null---}"

            res = self.session.request("POST", url=url, headers=getHeaders, data=payload)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.post_request("https://apps.atsondemand.com/templates/magneto/api/?action=getJobs")
            if isloaded:
                data = res.json()
                if len(data) > 0:
                    for link in data:
                        try:
                            jobObj = deepcopy(self.obj)
                            tokens = link['jid']
                            url = 'https://etcc.atsondemand.com/#/jobDescription/' + str(tokens)
                            jobObj['url'] = url
                            jobObj['title'] = link['job_title']
                            jobObj['location'] = link['fullStateName']
                            jobObj['description'] = link['jobdescription'] + "<br/><br/>" + link['jobbenefit'] + "<br/><br/>" + link['reqsexp']
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                        except (Exception, AttributeError, KeyError, ValueError) as ex:
                            pass
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))