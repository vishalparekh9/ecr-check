import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'WHITE_SHARK_MEDIA_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.whitesharkmedia.com/'

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
        self.domain = 'whitesharkmedia.com'
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
            JobId = []

            page = 0
            ispage = True
            while ispage:
                page = page + 1
                url = 'https://www.careers-page.com/white-shark-media?page='+str(page)+''
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, "lxml")
                    links = data.find("ul", {"class": "list-unstyled mx-3 mx-sm-4 mx-md-5 px-lg-5 pb-4"}).find_all("li", {"class": "media"})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            if link.find("a").get("href") is not None:
                                linkl = link.find("a").get("href")
                                if linkl.split("/job/")[1] not in JobId:
                                    JobId.append(linkl.split("/job/")[1])
                                    url = str("https://www.careers-page.com" + linkl)
                                    jobObj['url'] = url
                                    isloaded, res = self.get_request(url)
                                    if isloaded:
                                        data = BeautifulSoup(res.text, "lxml")
                                        jobObj['title'] = data.find("body").find("h1").text.replace("\r", "").replace("\n", "").strip()
                                        loc = data.find('div', {'class': 'banner d-flex flex-column justify-content-center align-items-center'}).find('span')
                                        if loc is not None:
                                            jobObj['location'] = loc.text.replace("\r", "").replace("\n", "").strip()
                                        else:
                                            jobObj['location'] = "United States"

                                        jobDesc = data.find("div", {"class": "mt-5 text-secondary"})
                                        jobObj['description'] = str(jobDesc)
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                            print(jobObj)

                                else:
                                    ispage = False
                                    break
                else:
                    print("Job Not Found")
            else:
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
