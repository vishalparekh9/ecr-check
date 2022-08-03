import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'SECOND_TO_NONE_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.second-to-none.com'

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
        self.domain = 'second-to-none.com'
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
            isloaded, res = self.get_request('https://www.second-to-none.com/careers/')
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                jobDataChunk = data.find("div", {"class": "sidebar_right"}).find_all('a')
                if jobDataChunk:
                    for link in jobDataChunk:
                        jobObj = deepcopy(self.obj)
                        try:
                            url = link.get('href')
                            jobObj['url'] = url
                            jobObj['title'] = link.find('b').text.replace("\r", "").replace("\n", "").strip()
                            jobObj['location'] = "United States"
                            isloaded, resJobData = self.get_request(url)
                            if isloaded:
                                jobDetail = BeautifulSoup(resJobData.text, "lxml")
                                jobObj['description'] = jobDetail.find("div", {"class": "main_content_left"})
                        except:
                            pass
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))