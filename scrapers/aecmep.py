import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj
#Token
token = 'AECMEP'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'http://www.aecmep.com/career.html' 

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
        self.domain = 'aecmep.com'
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
                jobDataChunk = data.find('div',{'class':'contact_content'})
                titles = []
                locations = []
                descriptions = []

                for title in jobDataChunk.find_all('h2',{'class':'highlight'}):
                    titles.append(title.text.strip())
                for location in jobDataChunk.find_all('div',{'class':'job'}):
                    locations.append(location.find_all('p')[0].text.split(',',1)[1])
                for description in jobDataChunk.find_all('div',{'class':'job'}):
                    descriptions.append(description)

                if jobDataChunk:
                    for t,l,d in zip(titles,locations,descriptions):
                        jobObj = deepcopy(self.obj)
                        jobObj['url'] = t
                        jobObj['title'] = t
                        jobObj['location'] = l
                        jobObj['description'] = d
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))