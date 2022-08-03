
import json
import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'JOB_APP_NETWORK_CHAMPPS_COM'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://apply.jobappnetwork.com/fun-eats-drinks'

        self.getHeaders = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '355',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
        }
        self.session = requests.session()
        self.domain = 'champps.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def post_request(self, url, payload):
        try:
            res = self.session.request("POST", url=url, headers=self.getHeaders, data=payload)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            page = -10
            isPage = True
            while isPage:
                page = page + 10
                url = 'https://prod-kong.internal.talentreef.com/apply/proxy-es/search-en-us/posting/_search'

                payload = '{"from":'+str(page)+',"size":10,"_source":["positionType","category","socialRecruitingAttribute1","description","address","jobId","clientId","clientName","brandId","location","internalOrExternal","url"],"query":{"bool":{"filter":[{"terms":{"clientId.raw":["12782"]}},{"terms":{"brand.raw":["Baileys Sports Grille","Craft Republic","Champps Kitchen & Bar","Fox & Hound Sports Tavern","Fun Eats and Drinks, LLC","Lucky Bastards"]}},{"terms":{"internalOrExternal":[{"internalOrExternal":"externalOnly"}]}}]}},"sort":[{"positionType.raw":{"order":"asc"}}]}'
                isloaded, res = self.post_request(url, payload=payload)
                if isloaded:
                    links = json.loads(res.text)['hits']['hits']
                    if len(links) > 0:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            clientId = link['_source']['clientId']
                            jobId = link['_source']['jobId']
                            url = f"https://apply.jobappnetwork.com/clients/{clientId}/posting/{jobId}/en"
                            jobObj['url'] = url
                            jobObj['title'] = link['_source']['positionType']
                            jobObj['location'] = link['_source']['address']['city']
                            jobObj['description'] = str(link['_source']['description'])
                            if len(jobObj['description']) > 100:
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        isPage = False
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