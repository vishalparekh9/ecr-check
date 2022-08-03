from pydoc import isdata
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
#Token
token = 'ZTECHINC_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.ztek-inc.com/career/' 

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
        self.domain = 'ztek-inc.com'
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
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, 'lxml')
                mainurl = ''
                for frame in data.find_all('iframe'):
                    if '/Jobs/career/' in str(frame):
                        mainurl = frame.get('src')
                        break
                isdata = True
                page = 0
                while isdata:
                    isloaded, res = self.get_request(mainurl)
                    if isloaded:
                        data = BeautifulSoup(res.text, 'lxml')
                        links = data.find_all('div',{'class':'crs-listRow'})
                        if links:
                            for link in links:
                                try:
                                    jobObj = deepcopy(self.obj)
                                    url = link.find('a').get('onclick')
                                    url = url.replace("getJobDescription('","").replace("'","").replace(')','').strip()
                                    jobObj['url'] = 'https://careerportal.ceipal.com/jobs/career/'+url.split(',')[1]+'/' +url.split(',')[0] 
                                    url = 'https://careerportal.ceipal.com/Jobs/single_job_description/'+url.split(',')[0]+'/' +url.split(',')[1] +'/0/null/0'
                                    isloaded, jobres = self.get_request(url)
                                    jobDetail =  BeautifulSoup(jobres.text, 'lxml')
                                    if isloaded:
                                        jobObj['title'] = jobDetail.find('div',{'class':'crsJT'}).text.strip()
                                        jobObj['location'] = jobDetail.find('div',{'class':'crsJAd'}).text.strip()
                                        jobObj['description'] =str(jobDetail.find(text='Overview').parent.parent)
                                except:
                                    pass
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                        else:
                            print('No Job Data Found!')
                            isdata = False
                        if data.find('a',{'rel':'next'}):
                            mainurl = 'https://careerportal.ceipal.com' + data.find('a',{'rel':'next'}).get('href')
                            page = page + 1
                            print("Collecting next page from: " + mainurl)
                        else:
                            isdata = False
                        
                        if page > 100:
                            break
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))