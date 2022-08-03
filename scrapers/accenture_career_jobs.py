import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj
# Token
token = 'ACCENTURE_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://accenture.com/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Content-Type': 'application/json',
            'Cookie': 'ASP.NET_SessionId=00cyilapzk4hnvejkj2a3su3'

        }
        self.session = requests.session()
        self.domain = 'accenture.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def get_request(self, url, payload):
        try:
            self.session = requests.session()
            res = self.session.request("POST", url, headers=self.getHeaders, data=payload)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            page = 0
            isPage = True
            urls = []
            while isPage:
                page = page + 10
                print("collecting page" + str(page))
                payload = json.dumps({
                    "f": page,
                    "s": 9,
                    "k": "",
                    "lang": "en",
                    "cs": "us-en",
                    "df": "[{\"metadatafieldname\":\"skill\",\"items\":[]},{\"metadatafieldname\":\"location\",\"items\":[]},{\"metadatafieldname\":\"postedDate\",\"items\":[{\"term\":\"past month\",\"selected\":true}]},{\"metadatafieldname\":\"travelPercentage\",\"items\":[]},{\"metadatafieldname\":\"jobTypeDescription\",\"items\":[]},{\"metadatafieldname\":\"businessArea\",\"items\":[{\"term\":\"industry x\",\"selected\":true},{\"term\":\"technology\",\"selected\":true}]},{\"metadatafieldname\":\"specialization\",\"items\":[]},{\"metadatafieldname\":\"workforceEntity\",\"items\":[]},{\"metadatafieldname\":\"yearsOfExperience\",\"items\":[]}]",
                    "c": "USA",
                    "sf": 1,
                    "syn": False,
                    "isPk": False,
                    "wordDistance": 0,
                    "userId": ""
                })

                url = 'https://www.accenture.com/api/sitecore/JobSearch/FindJobs'
                isloaded, res = self.get_request(url, payload)
                if isloaded:
                    try:
                        links = res.json()['documents']
                        if len(links) > 0:
                            for link in links:
                                jobObj = deepcopy(self.obj)
                                try:
                                    jobObj['url'] = url
                                    jobObj['title'] = str(link['title'])
                                    jobObj['location'] = str(link['location'][0])
                                    try:
                                        url = '' + str(link['jobDetailUrl']).replace("{0}/", '')
                                        if url not in urls:
                                            urls.append(url)
                                            isloaded, res = self.get_request(url, '{}')
                                            if isloaded:
                                                jobDetails = BeautifulSoup(res.text, 'lxml')
                                                jsonData = json.loads(str(jobDetails.find_all('script', {'type': 'application/ld+json'})[1].text))
                                                jobObj['description'] = str(jsonData[0]['description'])
                                        else:
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                        else:
                            print('Job Not Found!')
                            isPage = False
                            break
                    except:
                        isPage = False
                        pass
                else:
                    print('Job Not Found!')
                    isPage = False
                    break

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
