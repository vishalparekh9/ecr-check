import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'WCDGROUP_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://wcdgroup.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'wcdgroup.com'
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
            url = 'http://www.wcdgroup.com/contact/careers/'
            isloaded, res = self.get_request(url)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                links = data.find_all('div', {"class": "wpb_text_column wpb_content_element ui-blue"})
                desc = data.find_all('div', {'class': 'wpb_text_column wpb_content_element'})
                descCount = 1
                if links:
                    for link in links:
                        if link.find('p') is not None:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = url
                            jobObj['location'] = "United States"
                            jobObj['title'] = link.find('p').text.replace('\n', '').replace('\r', '').strip()
                            jobObj['description'] = str(desc[descCount])
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                                descCount = descCount + 1
                else:
                    print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
