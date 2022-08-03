from random import betavariate
import re
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json
from index import get_obj

token = 'UBER_CAREER'
class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.uber.com/us/en/careers/list/'

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
            'application/json',
            'Content-Type': 'application/json',
            'x-csrf-token': 'x'
        }
        self.session = requests.session()
        self.domain = 'uber.com'
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
    def post_request(self, url, page):
        try:
            params = '{"params":{"location":[],"department":[],"team":[],"programAndPlatform":[],"lineOfBusinessName":[]},"limit":10,"page":'+str(page)+'}'
            res = self.session.post(url, headers=self.postHeader, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False
    def process_logic(self):
        try:
            isdata = True
            page = 1
            oldurl = ''
            while isdata:
                isloaded, res = self.post_request('https://www.uber.com/api/loadSearchJobsResults?localeCode=en', page)
                page = page + 1
                print("collecting page: " + str(page))
                if not isloaded:
                    isdata = False
                    break
                if 'data' not in res.json(): break
                if 'results' not in res.json()['data']: break
                if len(res.json()['data']['results']) == 0: break
                objs = res.json()['data']['results']
                for obj in objs:
                    try:
                        jobObj = deepcopy(self.obj)
                        url = 'https://www.uber.com/global/en/careers/list/' + str(obj['id'])
                        jobObj['url'] = url
                        jobObj['title'] = obj['title']
                        jobObj['description'] = '<p>' +obj['description'] + '</p>'
                        try:
                            c = 0
                            for loc in obj['allLocations']:
                                if c == 0:
                                    jobObj['location'] += loc['city']+ ', ' + loc['region']
                                else:
                                    jobObj['location'] += ' | ' + loc['city'] + ', ' + loc['region']
                        except:
                            pass
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)
                    except:
                        pass
        except Exception as e:
            print(e)
            self.iserror = True
            isdata = False

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))