import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'NATUS_TALEO_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'http://natus.com/'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://phg.tbe.taleo.net/phg02/ats/careers/v2/searchResults?org=NATUS&cws=51',
            'Cookie': 'JSESSIONID=ADBCF2D7BA26D8B6998D99B9170FED53'
        }
        self.session = requests.session()
        self.domain = 'natus.com'
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
            page = -10
            ispage = True
            while ispage:
                page = page + 10
                url = f'https://phg.tbe.taleo.net/phg01/ats/careers/v2/searchResults?next&rowFrom={page}&act=null&sortColumn=null&sortOrder=null&currentTime=1652680339711'
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('div', {"class": "oracletaleocwsv2-accordion oracletaleocwsv2-accordion-expandable clearfix"})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = link.find("a").get("href")
                            jobObj['url'] = url
                            jobObj['title'] = link.find('h4').text.replace("\r", "").replace("\n", "").strip()

                            loc = link.find('div', {"class": "oracletaleocwsv2-accordion-head-info"}).find("div").text.replace("\r", "").replace("\n", "").strip()
                            jobObj['location'] = " ".join(loc.split())
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, 'lxml')
                                jobDesc = data.find("div", {"name": "cwsJobDescription"})
                                jobObj['description'] = str(jobDesc)
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        print("Job Not Found !")
                        ispage = False
                        break
                else:
                    print("Job Not Found")
                    ispage = False
            else:
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
