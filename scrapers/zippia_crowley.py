import time
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import json
import re
import os
import common as cf
# Token
token = 'ZIPPIA_CROWLEY_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.location = 'crowley'
        self.getHeaders = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8'
        }

        self.htmlHeaders = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        }

        self.session = requests.session()
        self.domain = 'zippia.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def html_request(self, url):
        co = 0
        while True:
            try:
                res = self.session.get(url, headers=self.htmlHeaders)
                if 'Website temporarily offline'.lower() not in res.text.lower():
                    return True, res
                print("Website temporarily offline")
            except Exception as e:
                print(e)
            co = co + 1
            time.sleep(0.5) 
            if co > 5:
                break
        return False, False

    def post_request(self, params):
        try:
            time.sleep(0.2)
            url = 'https://www.zippia.com/api/jobs/'
            res = self.session.post(url, headers=self.getHeaders, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def scrapDomain(self, company):
        try:
            link = cf.domain_finder(company)
            if link: return link
            url ='https://www.zippia.com/autocomplete/company/?searchString=' + company +'&indexableOnly=true'
            isloaded, res = self.html_request(url)
            if len(res.json()) > 0:
                for jn in res.json():
                    if jn['companyName'].strip().lower() == company.strip().lower():
                        url = 'https://www.zippia.com' + jn['zippiaCppUrl']
                        try:
                            isloaded, res = self.html_request(url)
                            soup = BeautifulSoup(res.text, 'lxml')
                            link = soup.find('div',{'class':'col-12 JobCompanyInfoParameter companyDomain'}).find('span').find('p').text
                            link = link.lower().replace('http://','').replace('https://','').replace('www.','')
                            link = link.split('?')[0]
                            link = link.split('/')[0]
                            return link
                        except:
                            pass
        except (AttributeError, KeyError, Exception, ValueError) as e:
            pass
        #link = cf.domain_finder(company)
        #if link: return link
        return 'zippia.com'

    
    def get_page_details(self, links):
        try:
            self.allJobs = []
            for link in links:
                time.sleep(0.1)
                jobObj = deepcopy(self.obj)
                jobObj['url'] = link['OBJurl']
                jobObj['title'] = link['OBJtitleDisplay']
                jobObj['company'] = link['companyName']
                try:
                    jobObj['location'] = link['location'] + ', '+link['OBJcountry']
                except:
                    pass
                jobObj['description'] = link['OBJdesc']
                jobObj['domain'] = self.scrapDomain(jobObj['company'])
                if jobObj['title'] != '' and jobObj['url'] != '':
                    self.allJobs.append(jobObj)
                    print(jobObj['title'])
        except:
            pass
    
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

    def find_data(self, res, key):
        try:
            searchloc = ''
            try:
                searchloc += '"city":' + '"'+ res.text.split('"city":')[1].split(',')[0].replace('"','') + '", '
            except:
                pass
            try:
                searchloc += '"state":' + '"' + res.text.split('"stateAbbr":')[1].split(',')[0].replace('"','') +'"'
            except:
                pass
            previoushas = []
            while True:
                try:
                    time.sleep(0.2)
                    print("Collecting next page")
                    params = '{"fetchJobDesc":true,"numJobs":30,"title":"'+key+'","locations":[{'+searchloc+'}],"postingDateRange":"1d","dismissedListingHashes":[],"previousListingHashes": '+str(previoushas).replace("'",'"')+'}'
                    isloaded, res = self.post_request(params)
                    if isloaded:
                        if 'jobs' not in res.json(): break
                        if len(res.json()['jobs']) == 0: break
                        for jn in res.json()['jobs']:
                            previoushas.append(jn['listingHash'])
                        self.get_page_details(res.json()['jobs'])
                        cf.insert_rows(self.allJobs, self.site, self.iserror, self.domain, False)
                except:
                    pass
                #break #remove this 
        except:
            pass

    def search_keyword(self, key, type):
        try:
            keywords = []
            url ='https://www.zippia.com/autocomplete/'+type+'/?searchString=' + key
            isloaded, res = self.html_request(url)
            if len(res.json()) > 0:
                co = 0
                for k in res.json():
                    keywords.append(k['name'].strip())
                    co = co + 1
                    if co >= 1:
                        break
        except:
            pass
        return keywords

    def process_logic(self):
        try:
            locations = self.search_keyword(self.location,'location')
            keywords = self.read_keywords()
            for key in keywords:
                time.sleep(0.2)
                searchkeys = self.search_keyword(key,'source')
                for search in searchkeys:
                    for location in locations:
                        time.sleep(0.2)
                        keyword = search
                        search = search.lower().replace(' ','-').replace('.','').replace(',','')
                        location = location.lower().replace(' ','-').replace('.','').replace(',','')
                        print("Collecting jobs for: " + search + ' :-: ' + location)
                        searchurl = 'https://www.zippia.com/'+search+'-'+location+'-jobs/'
                        isloaded, res  = self.html_request(searchurl)
                        if isloaded:
                            self.find_data(res, keyword)
                        # return
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))