import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'WAYNEBROTHERS_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.waynebrothers.com/careers/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'waynebrothers.com'
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
            url = 'https://portal.waynebrothers.com/Careers/GetJobReqSearchExternal'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = res.json()
                links = data
                if len(links) > 0:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = f"https://portal.waynebrothers.com/Careers/JobDetails/{link['ReqID']}?openModal=N"
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(f"https://portal.waynebrothers.com/Careers/GetReqDetails?reqID={link['ReqID']}&reqApplyToken=null")
                        if isloaded:
                            try:
                                jobDetail = jobres.json()
                                jobObj['title'] = link['PositionTitle']
                                jobObj['location'] = link['City'] + ", " + link['State']
                                jobObj['description'] = jobDetail['PositionDesc'] + "\n\n" + jobDetail['PositionRequirements'] + "\n\n" + jobDetail['PositionNotes']
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                            except:
                                pass
                else:
                    print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
