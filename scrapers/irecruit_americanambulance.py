import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'IRECRUITER_US_AMERICAN_AMBULANCE'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.americanambulance.com'

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
        self.domain = 'americanambulance.com'
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
            url = f'https://www.irecruit-us.com/index.php?OrgID=I20190410'
            print(url)
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find_all("a")
                for link in links:
                    try:
                        jobObj = deepcopy(self.obj)
                        url = f"" + str(link.get("href")).replace("amp;", "")
                        if "OrgID=" in url:
                            jobObj['title'] = link.text.replace("\r", "").replace("\n", "").replace("\t", "").strip()
                            if "," in jobObj['title']:
                                jobObj['title'] = jobObj['title'].split(",")[0].replace("Part-time", " ")
                            jobObj['url'] = url
                            isloaded, jobRes = self.get_request(url)
                            if isloaded:
                                jobData = BeautifulSoup(jobRes.text, "lxml")
                                jobObj['description'] = str(jobData.find("div", {"id": "page-wrapper"}))
                                jobObj['location'] = jobData.find("div", {"id": "page-wrapper"}).find("p").text.replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "").split("Location:")[1].strip()
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