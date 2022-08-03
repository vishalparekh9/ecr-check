import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'E3APPLICANTS_ALEXANDERYOUTHNETWORK_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.alexanderyouthnetwork.org'

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
        self.domain = 'alexanderyouthnetwork.org'
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
            url = f'https://alexanderyouthnetwork.e3applicants.com/careers/'
            print(url)
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find_all("div", {"class": "row JobPostRow"})
                if len(links) > 0:
                    for link in links:
                        try:
                            jobObj = deepcopy(self.obj)
                            url = "https://alexanderyouthnetwork.e3applicants.com" + str(link.find("a").get("href"))
                            jobObj['title'] = link.find("span", {"class": "title"}).text.replace("\r", "").replace("\n", "").replace("\t", "").strip()
                            jobObj['location'] = link.find("small").text.replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "").replace("Full Time", "").replace("Part Time", "").strip()
                            jobObj['url'] = url
                            isloaded, jobRes = self.get_request(url)
                            if isloaded:
                                jobData = BeautifulSoup(jobRes.text, "lxml")
                                jobObj['description'] = str(jobData.find("div", {"class": "col-lg-8 col-lg-offset-2 divMainContentArea"}))
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
