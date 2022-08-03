import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'ZIMBRA_TALEO'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://zimbra.com'

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
        self.domain = 'zimbra.com'
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
            url = 'https://phh.tbe.taleo.net/phh04/ats/careers/v2/searchResults?org=SYNACOR&cws=39'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('div', {'class': 'oracletaleocwsv2-accordion-head-info'})
                if links:
                    for link in links:
                        jobObj = deepcopy(self.obj)
                        url = str(link.find('a', {'class': 'viewJobLink'}).get('href'))
                        jobObj['url'] = url
                        jobObj['domain'] = self.domain
                        jobObj['title'] = link.find('h4').text.replace("\r", "").replace("\n", "").strip()
                        jobObj['location'] = link.find_all('div')[1].text.replace("\r", "").replace("\n", "").strip()
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            data = BeautifulSoup(res.text, 'lxml')
                            jobDesc = str(data.find('div', {'name': 'cwsJobDescription'}))
                            jobObj['description'] = jobDesc
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)


            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
