import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'WESCO_ORACLE_CLOUD_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://wesco.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'wesco.com'
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
            page = -100
            isPage = True
            while isPage:
                page = page + 100
                url = f'https://eklm.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX,facetsList=LOCATIONS;WORK_LOCATIONS;TITLES;CATEGORIES;ORGANIZATIONS;POSTING_DATES;FLEX_FIELDS,limit=100,offset={page}'
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = res.json()['items'][0]['requisitionList']
                    links = data
                    if len(links) > 0:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = link['Title']
                            jobObj['location'] = link['PrimaryLocation']
                            jobId = link['Id']
                            url = f"https://eklm.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/requisitions/preview/{jobId}"
                            url = url
                            descUrl = f'https://eklm.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails?expand=all&onlyData=true&finder=ById;Id="{jobId}",siteNumber=CX'
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(descUrl)
                            if isloaded:
                                jobDetail = jobres.json()['items'][0]['ExternalDescriptionStr']
                                jobObj['description'] = str(jobDetail)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        isPage = False
                        break
                else:
                    print("Job not Found!")
            else:
                print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
