import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
import json
from index import get_obj
#Token
token = 'ICIMS_BARNARDINC'

class CRAWLER(object):
    def __init__(self):
        self.host = 'https://jobs-barnard-inc.icims.com'
        self.baseUrl =  self.host + '/jobs/search?pr=0&in_iframe=1&mobile=false&width=809&height=500&bga=true&needsRedirect=false&jan1offset=330&jun1offset=330' 

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
        self.domain = 'barnard-inc.com'
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
            isdata = True
            page = 0
            while isdata:
                url = self.host + '/jobs/search?pr='+str(page)+'&in_iframe=1&mobile=false&width=809&height=500&bga=true&needsRedirect=false&jan1offset=330&jun1offset=330'
                isloaded, res = self.get_request(url)
                page = page + 1
                print("collecting page: " + str(page))
                if isloaded:
                    isdata = False
                    data = BeautifulSoup(res.text, 'lxml')
                    links = data.find_all('script',{'type':'text/javascript'})
                    if links:
                        for link in links:
                            jsn = ''
                            if 'jobImpressions' in link.text:
                                print("found")
                                try:
                                    isdata = True
                                    jsn = link.text.strip().split('];')[0]+']'
                                    jsn = jsn.split('jobImpressions')[1].strip().replace('= ','').strip()
                                    jsn = json.loads(jsn)
                                except Exception as e:
                                    print(e)
                                    jsn = ''
                            else:
                                continue
                            if jsn == '':
                                isdata = False
                                continue
                            if len(jsn) == 0:
                                isdata = False
                                continue
                            for job in jsn:
                                jobObj = deepcopy(self.obj)
                                url = self.host + '/jobs/'+str(job['idRaw'])+'/dispute-specialist/job?mobile=false&width=809&height=500&bga=true&needsRedirect=false&jan1offset=330&jun1offset=330&in_iframe=1'
                                jobObj['url'] = url
                                match, resdetail = self.get_request(url)
                                if match:
                                    soup = BeautifulSoup(resdetail.text, 'lxml')
                                    jobObj['title'] = soup.find('h1').text.strip()
                                    jobObj['location'] = job['location']['city'] +', ' + job['location']['state']
                                    jobObj['location'] = jobObj['location'].replace('not set,', '')
                                    jobObj['location'] = jobObj['location'].replace('not set', '')
                                    if jobObj['location'].strip() == '':
                                        try:
                                            jobObj['location'] = soup.find('div',{'class':'col-xs-6 header left'}).find_all('span')[1].text.strip()
                                        except:
                                            jobObj['location'] = 'United States'
                                            pass
                                    regex = re.compile('.*iCIMS_InfoMsg.*')
                                    descs = soup.find_all('div',{'class':regex})
                                    h2s = soup.find_all('h2',{'class':regex})
                                    for (desc,h2) in [(desc,h2) for desc in descs for h2 in h2s]:
                                        jobObj['description'] += str(h2)
                                        jobObj['description'] += str(desc)
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                    else:
                        print('No Job Data Found!')
                        isdata = False
                else:
                    isdata = False
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))