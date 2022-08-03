import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'IKCONTECH_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careerportal.ceipal.com/jobs/listing/NDU3NA==//' 

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
        self.domain = 'ikcontech.com'
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
            # regex = re.compile('.*job-desc-block.*')
            # descs = jobDetail.find_all('div',{'class':regex})
            page = 1
            isdata = True
            pageurl = self.baseUrl
            while isdata and pageurl !='':
                print("collecting page: " + str(page))
                page = page + 1
                isloaded, res = self.get_request(pageurl)
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('div',{'class':'crs-listRow'})
                    if links:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            url = link.find('a').get('onclick')
                            jobObj['title'] = link.find('a').text.strip().replace('&nbsp;','')
                            jobObj['location'] = link.find('div',{'class':'crsL-title-2'}).text.strip()
                            url = 'https://careerportal.ceipal.com/Jobs/single_job_description/' + url.split("'")[1] +'/'+ url.split("'")[3]
                            jobObj['url'] = url
                            isloaded, jobres = self.get_request(url)
                            jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                            if isloaded:
                                jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                try:
                                    jobObj['description'] = str(jobDetail.find(text='Overview').parent.parent)
                                except:
                                    pass
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                    else:
                        print('No Job Data Found!')
                try:
                    args = data.find_all(text=str(page))
                    pageurl = ""
                    for a in args:
                        if a.parent.name == 'a':
                            pageurl = 'https://careerportal.ceipal.com' + a.parent.get('href')
                except:
                    isdata = False
                    pass
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))