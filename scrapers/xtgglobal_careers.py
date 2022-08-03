import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'XTGGLOBAL_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.xtgglobal.com/careers/job-openings/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.session = requests.session()
        self.domain = 'xtgglobal.com'
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
            isloaded, resJobData = self.get_request("https://www.xtgglobal.com/careers/job-openings/")
            if isloaded:
                jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                jobData = jobDetails.find('div', {"class": "content entry"})
                aTag = jobData.find_all("h3")
                if len(aTag) > 0:
                    for link in aTag:
                        jobObj = deepcopy(self.obj)
                        tokens = link.find("a").get('href')
                        jobUrl = str(tokens)
                        jobObj['url'] = jobUrl
                        isloaded, resJobDetails = self.get_request(jobUrl)
                        if isloaded:
                            jobDetail = BeautifulSoup(resJobDetails.text, 'lxml')
                            jobObj['title'] = str(link.find('a').text.strip())
                            if "–" in jobObj['title']:
                                jobObj['location'] = str(jobObj['title']).split("–")[1]
                            else:
                                jobObj['location'] = "United States"

                            jobObj['description'] = str(jobDetail.find('div', {'class': 'content entry'}).text.strip())

                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)
                else:
                    print('No Job Data Found!')
            else:
                print('No Job Data Found!')

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))