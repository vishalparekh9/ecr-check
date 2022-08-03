import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import os
import time
import common as cf
#Token
token = 'INDEED_MATANUSKASUSITNA_BOROUGH'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.indeed.com/jobs?l=Matanuska-Susitna Borough^ US&fromage=1&radius=50'.replace('^ US','')

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
        self.domain = 'indeed.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
    def get_request(self, url):
        c = 0
        while True:
            try:
                res = self.session.get(url, headers=self.getHeaders) #,proxies={'http':'socks5://127.0.0.1:9050', 'https':'socks5://127.0.0.1:9050'})
                if 'hcaptcha solve page' not in res.text.lower(): 
                    return True, res
            except Exception as e:
                print(e)
            print("Checking try again:" + str(c))
            time.sleep(0.5)
            c = c + 1
            if c > 3: break
        return False, False
    
    def read_keywords(self):
        keywords = []
        try:
            with open(os.getcwd() + "/keywords") as f:
                lineList = f.readlines()
                for line in lineList:
                    keywords.append(line.strip().strip())
        except:
            pass
        return keywords

    def get_details(self, links):
        self.allJobs = []
        try:
            for link in links:
                time.sleep(1)
                jobObj = deepcopy(self.obj)
                #find a details
                url = 'https://www.indeed.com/viewjob?jk=' + link.get('data-jk')
                jobObj['url'] = url
                jobObj['domain'] = "indeed.com"
                jobObj['company'] = "Indeed"
                found, resdetail = self.get_request(url)
                if found:
                    try:
                        soup = BeautifulSoup(resdetail.text, 'lxml')
                        jobObj['title'] = soup.find('h1').text.strip()
                        try:
                            jobObj['location'] = link.parent.parent.parent.find('div',{'class':'companyLocation'}).text.split('+')[0].strip()
                        except:
                            pass
                        try:
                            jobObj['location'] = jobObj['location'].replace(link.find('span',{'class':'more_loc_container'}).text,'')
                        except:
                            pass
                        try:
                            if jobObj['location'] == '':
                                jobObj['location'] = soup.find('title').text.replace(jobObj['title'],'').split('-')[1].strip()
                        except:
                            pass
                        regex = re.compile('.*jobsearch-JobComponent-description.*')
                        jobObj['description'] = str(soup.find('div',{'class':regex}))
                    except:
                        pass
                
                #find a company name
                try:
                    jobObj['company'] = link.parent.parent.parent.find('span',{'class':'companyName'}).text
                    link = cf.domain_finder(jobObj['company'])
                    if link: jobObj['domain'] = link
                    else:
                        print("no domain found")
                        url = 'https://www.indeed.com' +link.parent.parent.parent.find('span',{'class':'companyName'}).find('a').get('href')
                        found, resdetail = self.get_request(url)
                        soup = BeautifulSoup(resdetail.text, 'lxml')
                        link = soup.find('a',{'data-tn-element':'companyLink[]'}).get('href')
                        jobObj['company'] = soup.find('a',{'data-tn-element':'companyLink[]'}).text.replace("Opens in a new window","").replace("website","")
                        link = link.lower().replace('http://','').replace('https://','').replace('www.','')
                        link = link.split('?')[0]
                        link = link.split('/')[0]
                        jobObj['domain'] = link
                except:
                    pass

                if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['location'] != '':
                    jobObj['location'] = jobObj['location'] + ', United States'
                    self.allJobs.append(jobObj)
                    print(jobObj['location'])
                    print("************")

        except:
            pass
    def process_logic(self):
        try:
            keywords = self.read_keywords()
            for key in keywords:
                print("Searching Keyword: " + str(key))
                try:
                    page = 0
                    isdata = True
                    while isdata:
                        time.sleep(1)
                        url = self.baseUrl + "&start=" + str(page) + "&q="+str(key)
                        page = page + 10
                        print("collecting page: " + str(page))
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            soup = BeautifulSoup(res.text, 'lxml')
                            regex = re.compile('.*job_.*')
                            div = soup.find('div',{'id':'mosaic-provider-jobcards'})
                            if div == None: break
                            links = div.find_all('a',{'id':regex})
                            if len(links) == 0: break
                            next = soup.find('a',{'aria-label':'Next'})
                            if not next: isdata = False
                            self.get_details(links)
                            cf.insert_rows(self.allJobs, self.site, self.iserror, self.domain, False)
                        else:
                            isdata = False
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    obj = CRAWLER()
    obj.process_logic()