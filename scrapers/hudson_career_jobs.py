import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'HBC_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://hbc.com/'

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
        self.domain = 'hbc.com'
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
                url = f'https://www.careershbc.com/?search_BannerName=Hudson%27s+Bay+Company+(hbc)&search_JobCategory=All&search_State=All&search_City=All&search_PayFrequencyBasis=All&search_Remotetype=All&search_keyword=&page={page}'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    links = data.find_all("div", {"class": "row job-panel"})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = str("") + link.find("a", {"class": "btn btn-solid"}).get("href")
                            jobObj['url'] = url
                            jobObj['title'] = link.find("h4").text.replace("\r", "").replace("\n", "").strip()
                            locOdd = link.find("div", {"class": "col-md-4 col-sm-4"}).find("p").text.replace("Hudson's Bay Company (HBC) -", "").replace("\r", "").replace("                            ", " ").replace("\n", "").strip()
                            jobObj['location'] = str(locOdd)
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                jobDetails = BeautifulSoup(res.text, "lxml")
                                jobObj['description'] = str(jobDetails.find("div", {"id": "job-details-2"}))
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        isPage = False
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