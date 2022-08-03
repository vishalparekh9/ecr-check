import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import json

# Token
token = 'PAYCOMONLINE_ALLIEDORION_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.paycomonline.net/v4/ats/web.php/jobs?clientkey=DD307E1816EE028CECBA0D3C7374DF0C'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.session = requests.session()
        self.domain = 'allied-orion.com'
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
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find("div", {"class": "container mainContainer noMarginTop"}).find("script").text.replace('\n', "").replace('\r', "").strip()
                links = links.replace('var jobs = ', '').replace('}];', '}]')
                jsonLinks = json.loads(str(links))
                if jsonLinks:
                    for link in jsonLinks:
                        jobObj = deepcopy(self.obj)
                        url = str("https://www.paycomonline.net" + link['url'])
                        if url is not None:
                            jobObj['url'] = url
                            jobObj['title'] = link['title']
                            if link['location']['description'] == ' ':
                                jobObj['location'] = 'United States'
                            else:
                                jobObj['location'] = link['location']['description']
                            isloaded, res = self.get_request(url)
                            if isloaded:
                                data = BeautifulSoup(res.text, "lxml")
                                jobObj['description'] = str(data.find('div', {'name': 'description'}))
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))