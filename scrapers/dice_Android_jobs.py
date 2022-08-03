import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os
import common as cf
# Token
token = 'DICE_ANDROID_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.dice.com'
        self.jobTitle = "Android"
        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'origin': 'https://www.dice.com',
            'referer': 'https://www.dice.com/',
            'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'x-api-key': '1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8'
        }
        self.session = requests.session()
        self.domain = 'dice.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def get_request(self, url, type=""):
        try:
            googleHeaders = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
            }
            if len(type) > 1:
                res = self.session.get(url, headers=googleHeaders)
                return True, res
            else:
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
                page = page + 1
                print("Scraping for page ", page)
                url = 'https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search?q='+str(self.jobTitle)+'&locationPrecision=Country&latitude=37.09024&longitude=-95.712891&countryCode2=US&radius=30&radiusUnit=mi&page='+str(page)+'&pageSize=20&facets=employmentType%7CpostedDate%7CworkFromHomeAvailability%7CemployerType%7CeasyApply%7CisRemote&filters.postedDate=ONE&fields=id%7CjobId%7Csummary%7Ctitle%7CpostedDate%7CmodifiedDate%7CjobLocation.displayName%7CdetailsPageUrl%7Csalary%7CclientBrandId%7CcompanyPageUrl%7CcompanyLogoUrl%7CpositionId%7CcompanyName%7CemploymentType%7CisHighlighted%7Cscore%7CeasyApply%7CemployerType%7CworkFromHomeAvailability%7CisRemote&culture=en&recommendations=true&interactionId=0'
                isloaded, res = self.get_request(url)
                if isloaded:
                    if 'text/plain' in res.headers.get('content-type'): break
                    if 'data' not in res.json(): break
                    if len(res.json()['data']) == 0: break
                    for data in res.json()['data']:
                        jobObj = deepcopy(self.obj)
                        try:
                            title = data['title']
                            jobLocation = data['jobLocation']['displayName']
                            # postedDate = data['postedDate']
                            detailsPageUrl = data['detailsPageUrl']
                            companyPageUrl = data['companyPageUrl']
                            companyName = data['companyName']
                            jobObj['company'] = companyName
                            jobObj['url'] = detailsPageUrl
                            jobObj['title'] = title
                            jobObj['location'] = jobLocation

                            link = cf.domain_finder(jobObj['company'])
                            if link: jobObj['domain'] = link
                            if link == False:
                                isloaded, res = self.get_request(str(companyPageUrl))
                                if isloaded:
                                    data = BeautifulSoup(res.text, "lxml")
                                    companyDomainTxt = data.find("a", {"class": "clabel ctxt dice-btn-link undeline_URL"})
                                    if companyDomainTxt is not None:
                                        companyDomainUrl = data.find("a", {"class": "clabel ctxt dice-btn-link undeline_URL"}).get("href")

                                        companyDomainUrl = companyDomainUrl.lower().replace('http://', '').replace('https://', '').replace('www.', '').replace('/', '').replace('careers.', '').replace('jobs.', '')

                                        jobObj['domain'] = str(companyDomainUrl).strip()
                                    else:
                                        jobObj['domain'] = str("dice.com").strip()

                            isloaded, res = self.get_request(str(detailsPageUrl))
                            if isloaded:
                                data = BeautifulSoup(res.text, "lxml")
                                jobDetails = data.find("div", {"class": "container job-details"}).find("div", {"id": "jobdescSec"})

                                jobObj['description'] = str(jobDetails)
                        except:
                            pass
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                else:
                    print("Job Not Found")
                print(len(self.allJobs))
                cf.insert_rows(self.allJobs, self.site, False, self.domain, False)
                self.allJobs = []

            else:
                print("Job Not Found")
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()