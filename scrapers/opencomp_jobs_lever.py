
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'OPEN_COMP_JOBS_LEVER'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.opencomp.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.postHeader = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Accept':
                '*/*',
            'Content-Type': 'application/json',
        }
        self.session = requests.session()
        self.domain = 'opencomp.com'
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

    def post_request(self, url, params):
        try:
            # params = '{"limit":20,"offset":'+str(page)+',"appliedFacets":{},"searchText":""}'
            res = self.session.post(url, headers=self.postHeader, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def process_logic(self):
        try:
            isloaded, res = self.get_request("https://jobs.ashbyhq.com/opencomp")
            if isloaded:
                url = 'https://jobs.ashbyhq.com/api/non-user-graphql'
                params = '{"operationName":"ApiJobPostingBriefsWithIds","variables":{"organizationHostedJobsPageName":"opencomp"},"query":"query ApiJobPostingBriefsWithIds($organizationHostedJobsPageName: String!) {  jobPostingBriefs: jobPostingBriefsWithIds(    organizationHostedJobsPageName: $organizationHostedJobsPageName  ) {    id    title    departmentId    departmentName    locationId    locationName    employmentType    secondaryLocations {      ...JobPostingSecondaryLocationParts      __typename    }    __typename  }}fragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {  locationId  locationName  __typename}"}'
                isloaded, res1 = self.post_request(url, params)
                if isloaded:
                    if 'data' not in res1.json(): return
                    if 'jobPostingBriefs' not in res1.json()['data']: return
                    links = res1.json()['data']['jobPostingBriefs']
                    for job in links:
                        try:
                            jobObj = deepcopy(self.obj)
                            url = 'https://jobs.ashbyhq.com/opencomp/' + str(job['id'])
                            jobObj['url'] = url
                            jobObj['title'] = job['title']
                            jobObj['location'] = job['locationName']
                            posturl = 'https://jobs.ashbyhq.com/api/non-user-graphql'
                            params = '{"operationName":"ApiJobPosting","variables":{"organizationHostedJobsPageName":"opencomp","jobPostingId":"' + str(job['id'])+'"},"query":"query ApiJobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {  jobPosting(    organizationHostedJobsPageName: $organizationHostedJobsPageName    jobPostingId: $jobPostingId  ) {    id    title    departmentName    locationName    employmentType    descriptionHtml    isListed    applicationForm {      ...FormRenderParts      __typename    }    surveyForms {      ...FormRenderParts      __typename    }    secondaryLocationNames    __typename  }}fragment FormRenderParts on FormRender {  id  formControls {    identifier    title    __typename  }  errorMessages  sections {    title    descriptionHtml    fieldEntries {      ...FormFieldEntryParts      __typename    }    __typename  }  sourceFormDefinitionId  __typename}fragment FormFieldEntryParts on FormFieldEntry {  id  field  fieldValue {    ... on JSONBox {      ...JSONBoxParts      __typename    }    ... on File {      ...FileParts      __typename    }    ... on FileList {      files {        ...FileParts        __typename      }      __typename    }    __typename  }  isRequired  descriptionHtml  __typename}fragment JSONBoxParts on JSONBox {  value  __typename}fragment FileParts on File {  id  url  filename  __typename}"}'
                            isloaded, resdesc = self.post_request(posturl, params)
                            if isloaded:
                                if 'data' not in resdesc.json(): return
                                if 'jobPosting' not in resdesc.json()['data']: return
                                jobObj['description'] = resdesc.json()['data']['jobPosting']['descriptionHtml']
                            if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['description'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                        except:
                            pass
        except Exception as e:
            print('error')
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))