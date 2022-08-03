import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'WWNORTON_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://wwnorton.atsondemand.com/index.cfm?cid=512989&fuseaction=512989.viewjobs&buid=6680'

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
        self.domain = 'wwnorton.com'
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
                data = BeautifulSoup(res.text, 'lxml')
                aTag = data.find_all('a', {'class': 'myBtn col-md-4 text-center'})
                for link in aTag:
                    jobObj = deepcopy(self.obj)
                    token = str(link.get('href')).split("&build=")[0]
                    url = 'https://wwnorton.atsondemand.com/' + str(token)
                    jobObj['url'] = url
                    isloaded, resJobData = self.get_request(url)
                    if isloaded:
                        jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                        jobObj['title'] = str(jobDetails.find('h1').text.strip())
                        jobObj['location'] = str(
                            jobDetails.find('ul', {'class': 'list-unstyled'}).find_all('li')[1].text.split(':')[
                                1].strip())
                        for desc in jobDetails.find_all('h2'):
                            jobObj['description'] += str(desc.find_previous('div'))

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