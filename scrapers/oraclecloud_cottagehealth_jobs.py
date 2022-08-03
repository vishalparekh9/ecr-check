import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'ORACLECLOUD_COTTAGEHEALTH_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.mainurl = 'https://eglz.fa.us2.oraclecloud.com/CX'
        self.host = self.mainurl.split('/CX')[0]
        self.sitenumber = 'CX' + self.mainurl.split('/CX')[1]
        self.baseUrl =  self.host + '/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber='+self.sitenumber+',facetsList=LOCATIONS%3BWORK_LOCATIONS%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=50,offset=' 

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
        self.domain = 'cottagehealth.org'
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
            isdata = True
            page = 0
            while isdata:
                url = self.baseUrl + str(page)
                isloaded, res = self.get_request(url)
                page = page + 50
                print("collecting page: " + str(page))
                if isloaded:
                    if 'items' in res.json():
                        if len(res.json()['items']) == 0:
                            isdata = False
                            break
                        if 'requisitionList' not in res.json()['items'][0]:
                            isdata = False
                            break
                        if len(res.json()['items'][0]['requisitionList']) == 0:
                            isdata = False
                            break
                        for link in res.json()['items'][0]['requisitionList']:
                            jobObj = deepcopy(self.obj)
                            url =  self.host + '/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails?expand=all&onlyData=true&finder=ById;Id=%22'+str(link['Id'])+'%22,siteNumber=' + self.sitenumber
                            jobObj['url'] =  self.host + '/hcmUI/CandidateExperience/en/sites/'+self.sitenumber+'/requisitions/preview/'+ str(link['Id'])
                            isloaded, jobres = self.get_request(url)
                            if isloaded:
                                try:
                                    jobObj['title'] = jobres.json()['items'][0]['Title']
                                    jobObj['location'] = link['PrimaryLocation']
                                    jobObj['description'] = jobres.json()['items'][0]['ExternalDescriptionStr']
                                except:
                                    pass
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        isdata = False
                else:
                    isdata = False
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True
        
if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))