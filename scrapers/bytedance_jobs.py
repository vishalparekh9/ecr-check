from random import betavariate
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import json
from index import get_obj

token = 'BYTEDANCE_JOBS'
class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://jobs.bytedance.com/en/position?keywords='

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.postHeader = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Accept':
            'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'x-csrf-token': 'undefined',
            'website-path': 'en',
            'env': 'undefined'
        }
        self.session = requests.session()
        self.domain = 'bytedance.com'
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
    def post_request(self, url, params):
        try:
            #params = '{"limit":20,"offset":'+str(page)+',"appliedFacets":{},"searchText":""}'
            res = self.session.post(url, headers=self.postHeader, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    
    def process_logic(self):
        try:
            isloaded, res = self.get_request(self.baseUrl)
            token = None
            if isloaded:
                params = '{"portal_entrance":1}'
                url = 'https://jobs.bytedance.com/api/v1/csrf/token'
                isloaded, res1 = self.post_request(url, params)
                token = res1.cookies.get_dict()['atsx-csrf-token'].replace('%3D','=')
            if token:
                page = 0
                isdata = True
                self.postHeader['x-csrf-token'] = token
                while True:
                    url = 'https://jobs.bytedance.com/api/v1/search/job/posts?keyword=&limit=10&offset='+str(page)+'&job_category_id_list=&location_code_list=&subject_id_list=&recruitment_id_list=&portal_type=4&job_function_id_list=&portal_entrance=1'
                    params = '{"keyword":"","limit":10,"offset":'+str(page)+',"job_category_id_list":[],"location_code_list":[],"subject_id_list":[],"recruitment_id_list":[],"portal_type":4,"job_function_id_list":[],"portal_entrance":1}'
                    page = page + 10
                    isloaded, res1 = self.post_request(url, params)
                    if isloaded:
                        if 'data' not in res1.json(): break
                        if 'job_post_list' not in res1.json()['data']: break
                        if len(res1.json()['data']['job_post_list']) == 0: break
                        links = res1.json()['data']['job_post_list']
                        print(links[0]['title'])
                            
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = 'https://jobs.bytedance.com/en/position/' + str(link['id']) + '/detail'
                            jobObj['title'] = link['title']
                            jobObj['location'] = link['city_info']['en_name']
                            url = 'https://jobs.bytedance.com/api/v1/job/posts/7081047737223727397?portal_type=4&with_recommend=false&portal_type=4&with_recommend=false'
                            isloaded, resdesc = self.get_request(url)
                            if 'job_post_detail' in resdesc.json()['data']:
                                jobObj['description'] = resdesc.json()['data']['job_post_detail']['description']
                                jobObj['description'] = jobObj['description'] + '<br><b>Qualifications</b>' + resdesc.json()['data']['job_post_detail']['requirement']

                            if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['description'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj['title'])
        except Exception as e:
            print(e)
            self.iserror = True
            isdata = False

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))