import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'GRAVITYRESOURCES'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.gravityitresources.com'

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
        self.domain = 'gravityitresources.com'
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
            ispage = True
            while ispage:
                page = page + 1
                print("Scraping for page ", page)
                url = 'https://www.gravityitresources.com/job-search/?_paged='+str(page)+''
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    try:
                        links = data.find('ul', {'class': 'job_listings'}).find_all('li')
                        if links:
                            for link in links:
                                try:
                                    jobObj = deepcopy(self.obj)
                                    if link.find('a') is not None:
                                        url = str(link.find('a').get('href'))
                                        jobObj['url'] = url
                                        jobObj['title'] = link.find('h3').text.replace("\r", "").replace("\n", "").strip()
                                        jobObj['location'] = link.find('div', {'class': 'location'}).text.replace("\r", "").replace("\n", "").strip()
                                        isloaded, res = self.get_request(url)
                                        if isloaded:
                                            data = BeautifulSoup(res.text, 'lxml')
                                            jobDesc = data.find('div', {'class': 'fl-content fl-content-left col-md-8'})
                                            jobObj['description'] = str(jobDesc)
                                            if jobObj['title'] != '' and jobObj['url'] != '':
                                                self.allJobs.append(jobObj)
                                                print(jobObj)
                                except:
                                    pass
                    except:
                        ispage = False
                        print("Job Not Found!")
                else:
                    ispage = False
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
