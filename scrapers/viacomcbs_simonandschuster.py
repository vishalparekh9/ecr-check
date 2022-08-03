import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup


# Token
token = 'VIACOM_CBS_SIMON_AND_SCHUSTER_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.viacomcbs.com'

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
        self.domain = 'simonandschuster.com'
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
            page = -25
            isPage = True
            while isPage:
                page = page + 25
                url = 'https://careers.viacomcbs.com/tile-search-results/category/8711600/&startrow=' + str(
                    page) + ''
                print("Collecting for page ", page)
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('div', {"class": "col-md-12 sub-section sub-section-desktop hidden-xs hidden-sm"})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = str("https://careers.viacomcbs.com" + link.find('a').get("href")).strip()
                            jobObj['url'] = url
                            jobObj['title'] = link.find('h2').text.replace("\n", "").replace("\r", "").replace("\t", "").strip()
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, 'lxml')
                                jobDesc = str(data.find('div', {'class': 'jobDisplay'}))
                                jobObj['location'] = data.find('span', {'class': 'jobGeoLocation'}).text.replace("\n", "").replace("\r", "").replace("\t", "").strip()
                                jobObj['description'] = jobDesc
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        print("Job Not Found")
                        break
                else:
                    print("Job Not Found")
                    break
            else:
                print("Job Not Found")
                isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
    print(scraper.allJobs)