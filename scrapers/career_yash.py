from posixpath import islink
import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from index import get_obj

# Token
token = 'YASH_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://yash.com/'

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
        self.domain = 'yash.com'
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
            isPage = True
            urls = []
            while isPage:
                page = page + 10
                print("collecting page " + str(page))
                isloaded, res = self.get_request(f'https://careers.yash.com/search?q=&sortColumn=referencedate&sortDirection=desc&startrow={page}')
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('tr', {'class': "data-row"})
                    islinks = False
                    for link in links:
                        if link.find('a') is not None:
                            jobObj = deepcopy(self.obj)
                            try:
                                url = 'https://careers.yash.com' + str(link.find("a").get("href")).strip()
                                if url in urls:
                                    isPage = False
                                    break
                                urls.append(url)
                                islinks = True
                                jobObj['url'] = url
                                try:
                                    jobObj['title'] = str(link.find('a').text.strip())
                                    jobObj['location'] = str(link.find('span', {"class": "jobLocation"}).text.strip())
                                    isloaded, res = self.get_request(url)
                                    if isloaded:
                                        jobDetails = BeautifulSoup(res.text, 'lxml')
                                        jobObj['description'] = str(jobDetails.find('div', {'class': 'jobDisplay'}))
                                    else:
                                        print('No Job Data Found!')
                                except:
                                    pass
                            except:
                                pass
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                    if islinks == False:
                        break

                else:
                    isPage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))