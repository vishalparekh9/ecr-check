import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'CANDIDATE_CARE_JOBS_CENTRALEMS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://centralems.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'centralems.com'
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
            url = f'https://centralems.candidatecare.jobs/job_positions/browse'
            print(url)
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find("div", {"class": "panel-group"}).find_all("li")
                if len(links) > 0:
                    for link in links:
                        try:
                            jobObj = deepcopy(self.obj)
                            url = f"" + str(link.find("a").get("href"))
                            jobObj['title'] = link.find("a").text.replace("\r", "").replace("\n", "").replace("\t", "").strip()
                            if "," in jobObj['title']:
                                jobObj['title'] = jobObj['title'].split(",")[0].replace("Part-time", " ")
                            jobObj['location'] = link.find("span", {"class": "italic small"}).text.replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "").replace("Full Time", "").replace("Part Time", "").strip()
                            if "Full-time" in jobObj['location']:
                                jobObj['location'] = jobObj['location'].split("Full-time")[0].replace("Part-time", " ")

                            jobObj['url'] = url
                            isloaded, jobRes = self.get_request(url)
                            if isloaded:
                                jobData = BeautifulSoup(jobRes.text, "lxml")
                                jobObj['description'] = str(jobData.find("div", {"id": "page-content"}))

                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                        except (Exception, KeyError, AttributeError, ValueError) as e:
                            pass
            else:
                print("Job Not Found!")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))