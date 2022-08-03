import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'VERY_FI_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.veryfi.com'

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
        self.domain = 'veryfi.com'
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
            isloaded, res = self.get_request('https://www.veryfi.com/jobs/')
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                jobDataChunk = data.find_all('tr')
                if jobDataChunk:
                    for link in jobDataChunk:
                        jobObj = deepcopy(self.obj)
                        if link.find("a") is not None:
                            try:
                                url = link.find("a").get('href')
                                jobObj['url'] = url
                                jobObj['title'] = link.find_all("td")[0].text.replace("\r", "").replace("\n", "").strip()
                                jobObj['location'] = link.find_all("td")[1].text.replace("\r", "").replace("\n", "").strip()
                                isloaded, resJobData = self.get_request(url)
                                if isloaded:
                                    jobDetail = BeautifulSoup(resJobData.text, "lxml")
                                    jobObj['description'] = jobDetail.find("meta", {"property": "og:description"}).get("content")
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