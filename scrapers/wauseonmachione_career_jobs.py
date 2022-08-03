import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'ENTERTIMEONLINE_AWARETECH_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://secure6.entertimeonline.com/ta/rest/ui/recruitment/companies/|6040538/job-requisitions?offset=0&ein_id=&_=1652259075509'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'Accept':
                'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.session = requests.session()
        self.domain = 'wauseonmachine.com'
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
            url = self.baseUrl
            isloaded, res = self.get_request(url)
            if isloaded:
                data = res.json()['job_requisitions']
                links = data
                if len(links) > 0:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        jobObj['title'] = link['job_title']
                        jobObj['location'] = link['location']['country'] + ", " + link['location']['city'] + ", " + \
                                             link['location']['state']
                        jobId = link['id']
                        url = f"https://secure6.entertimeonline.com/ta/rest/ui/recruitment/companies/|6040538/job-requisitions/{jobId}?_=1652259075514"
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        try:
                            if isloaded:
                                jobDetails = jobres.json()
                                desc = jobDetails['job_description'] + "\n\n" + jobDetails['job_requirement']
                                if desc:
                                    jobObj['description'] = desc
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                        except:
                            pass
        except (Exception, BaseException, AttributeError, KeyError, ValueError) as ex:
            print("Job Not found")


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
