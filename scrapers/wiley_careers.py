
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import os

# Token
token = 'WILEY_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.wiley.com/'

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
        self.domain = 'wiley.com'
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
                url = f'https://backend.ascendify.com/jobsapi/showPublicJobsList/bwL0bd7JDsDkWmO/{page}?search_id=srch_0638816639&community_id=ccid_1b71001253&app=false&language=en'
                isloaded, res = self.get_request(url)
                if isloaded:
                    mainData = str(res.json()['page']).replace("[", "").replace("]", "").replace("\\'", "'").replace('\\"', '"').replace("\\n", "").replace("\\r", "").replace("\\t", "").replace("\\/", "/").strip()
                    rawData = BeautifulSoup(str(mainData), "lxml")
                    links = rawData.find_all("div", {"class": "asc-job-public-header clearfix"})
                    if len(links) > 0:
                        for data in links:
                            jobObj = deepcopy(self.obj)
                            url = data.find("a").get("href")
                            jobObj['url'] = url
                            jobObj['title'] = str(data.find("a").text)
                            jobObj['location'] = data.find("div", {"class": "muted asc-job-public-stats"}).text.split(":")[0].replace("Position Title", "").replace("Location", "")
                            jobId = str(url).split("/position/")[1].strip()
                            link_url = f"https://backend.ascendify.com/jobsapi/showJobListing/bwL0bd7JDsDkWmO/{jobId}?client_community_id=ccid_1b71001253&jobid={jobId}&board_id=&source_board=&language=en&success=undefined"
                            isloaded, res = self.get_request(link_url)
                            if isloaded:
                                rawRes = str(res.text).replace("[", "").replace("]", "").replace("\\'", "'").replace('\\"', '"').replace("\\n", "").replace("\\r", "").replace("\\t", "").replace("\\/", "/").strip()
                                data = BeautifulSoup(rawRes, 'lxml')
                                jobDesc = str(data.find('div', {'id': 'asc-job-location'}))
                                if jobDesc:
                                    jobObj['description'] = jobDesc
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                    else:
                        print("Job Not Found")
                        isPage = False
                        break
                else:
                    print("Job Not Found")
                    isPage = False
                    break
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
