
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOBS_SAAS_HR_DCHC'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://secure6.saashr.com/ta/rest/ui/recruitment/companies/%7C6098626/job-requisitions'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'dchc.org'
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
            page = -50
            isPage = True
            while isPage:
                page = page + 50
                print("Collecting for page ", page)
                url = f'https://secure6.saashr.com/ta/rest/ui/recruitment/companies/%7C6098626/job-requisitions?offset={page}&ein_id='
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = res.json()['job_requisitions']
                    if len(data) > 0:
                        for link in data:
                            jobObj = deepcopy(self.obj)
                            jobObj['title'] = link['job_title']
                            jobId = link['id']
                            url = f"https://secure6.saashr.com/ta/rest/ui/recruitment/companies/%7C6098626/job-requisitions/{jobId}"
                            jobObj['url'] = url
                            if link['location'] is not None:
                                jobObj['location'] = link['location']['city'] + ", " + link['location']['country']
                            else:
                                jobObj['location'] = "United States"

                            isloaded, res = self.get_request(url)
                            if isloaded:
                                jobData = res.json()
                                jobDesc = jobData['job_description'] + "<br />" + jobData['job_requirement'] + "<br />"
                                jobObj['description'] = str(jobDesc)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        print("Job Not Found")
                        ispage = False
                        break
            else:
                print("Job Not Found")
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))