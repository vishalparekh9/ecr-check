import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json
import time
from urllib3 import Retry
from index import get_obj

token = 'TECHMAHINDRA_JOBS'
class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.techmahindra.com/CurrentOpportunity.aspx'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        self.postHeader = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Accept':
            '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-MicrosoftAjax': 'Delta=true'
        }
        self.session = requests.session()
        self.domain = 'getfreemo.com'
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
        
    def post_request(self, params):
        try:
            url = 'https://careers.techmahindra.com/CurrentOpportunity.aspx'
            res = self.session.post(url, headers=self.postHeader, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    
    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                isdata = True
                page = 100
                soup = BeautifulSoup(res.text, 'lxml')
                __VIEWSTATE = soup.find('input',{'name':'__VIEWSTATE'}).get('value')
                __VIEWSTATEGENERATOR =  soup.find('input',{'name':'__VIEWSTATEGENERATOR'}).get('value')
                __EVENTVALIDATION = soup.find('input',{'name':'__EVENTVALIDATION'}).get('value')
                while isdata:
                    params = {
                    "ctl00$ContentPlaceHolder1$ToolkitScriptManager1": "ctl00$ContentPlaceHolder1$UpdatePanel2|ctl00$ContentPlaceHolder1$rptPager$ct"+str(page)+"$lnkPage",
                    "ctl00_ContentPlaceHolder1_ToolkitScriptManager1_HiddenField": "",
                    "ctl00$ContentPlaceHolder1$ddlCountry": "All Countries",
                    "ctl00$ContentPlaceHolder1$ddlState": 0,
                    "ctl00$ContentPlaceHolder1$ddlCity": 0,
                    "ctl00$ContentPlaceHolder1$ddlTotExpYears": 0,
                    "__EVENTTARGET": "ctl00$ContentPlaceHolder1$rptPager$ct"+str(page)+"$lnkPage",
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS": "",
                    "__VIEWSTATE": __VIEWSTATE,
                    "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                    "__EVENTVALIDATION": __EVENTVALIDATION,
                    "__ASYNCPOST": "true",
                    "":""
                    }
                    isloaded, res1 = self.post_request(params)
                    print("Collecting page: " + str(page))
                    time.sleep(2)
                    page = page + 1
                    soup1 = BeautifulSoup(res1.text, 'lxml')
                    links = soup1.find_all('div',{'class':'joblist'})
                    if len(links) == 0: break
                    print(params['__EVENTTARGET'])
                    print(links[0].find('h3').text)
                    for link in links:
                        continue
                        jobObj = deepcopy(self.obj)
                        url = 'https://careers.techmahindra.com/' + link.find('a').get('href')
                        jobObj['url'] = url
                        jobObj['title'] = link.find('h3').text.strip()
                        try:
                            jobObj['location'] = link.find('p').text.strip().split('Location:')[1].strip()
                        except:
                            pass
                        isloaded, resdesc = self.get_request(url)
                        if isloaded:
                            data = BeautifulSoup(resdesc.text, 'lxml')
                            try:
                                jobObj['location'] =data.find('li',{'class':'loctn'}).text.strip().replace('Location:','').strip()
                                jobObj['description'] = str(data.find(text='Job Summary').parent.find_next_sibling('p'))
                            except:
                                pass
                        print(jobObj)
                        return
                        if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['description'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj['title'])
                    __VIEWSTATE = res1.text.split('__VIEWSTATE|')[1].split('|')[0]
                    __VIEWSTATEGENERATOR = res1.text.split('__VIEWSTATEGENERATOR|')[1].split('|')[0]
                    __EVENTVALIDATION = res1.text.split('__EVENTVALIDATION|')[1].split('|')[0]
                    
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))