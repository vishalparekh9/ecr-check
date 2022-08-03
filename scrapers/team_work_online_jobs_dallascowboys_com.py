
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'TEAM_WORK_ONLINE_CAREER_JOBS_DALLASCOWBOYS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.dallascowboys.com'

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
        self.domain = 'dallascowboys.com'
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
            page = 0
            isPage = True
            while isPage:
                page = page + 1
                url = f'https://www.teamworkonline.com/jobs-in-sports?employment_opportunity_search%5Bquery%5D=Dallas+Cowboys&commit=Search&page={page}'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    links = data.find_all("div", {"class": "result-item recent-job"})
                    if len(links) > 0:
                        for link in links:
                            try:
                                jobObj = deepcopy(self.obj)
                                url = f"https://www.teamworkonline.com" + str(link.find("div", {"class": "result-content"}).find("a").get("href"))
                                jobObj['title'] = link.find("h3").text.strip()
                                jobObj['location'] = link.find("span").text.replace("Full Time", "").replace("Part Time", "").strip()

                                if "Jobs in" in jobObj['location']:
                                    jobObj['location'] = jobObj['location'].split("Jobs in")[1].strip()

                                jobObj['url'] = url
                                isloaded, jobRes = self.get_request(url)
                                if isloaded:
                                    jobData = BeautifulSoup(jobRes.text, "lxml")
                                    jobObj['description'] = jobData.find("div", {"class": "opportunity-preview__body"})
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                            except (Exception, KeyError, AttributeError, ValueError) as e:
                                pass
                    else:
                        break
                else:
                    print("Job Not Found!")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))