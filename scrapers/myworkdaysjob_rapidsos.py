import requests
from copy import deepcopy
import json
from index import get_obj

token = 'MYWORKDAYSJOB_RAPIDSOS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://rapidsos.wd1.myworkdayjobs.com/RapidSOS'

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
                'application/json',
            'Content-Type': 'application/json',
        }
        self.session = requests.session()
        self.domain = 'rapidsos.com'
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
            params = '{"limit":20,"offset":' + str(page) + ',"appliedFacets":{},"searchText":""}'
            res = self.session.post(url, headers=self.postHeader, data=params)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def extract_key(self, elem, key):
        '''
        Attempts to extract the object at the given key from the nested json document
        Assuming nesting is done by dict/list objects

        Input:
            elem: start of nested json document
            key: target key to find
        Returns:
            elem[key] if found
            None if key does not exist
        '''
        if isinstance(elem, dict):
            if key in elem:
                return elem[key]
            for k in elem:
                item = self.extract_key(elem[k], key)
                if item is not None:
                    return item
        elif isinstance(elem, list):
            for k in elem:
                item = self.extract_key(k, key)
                if item is not None:
                    return item
        return None

    def get_page_URL(self, res, url):
        try:
            end_points = self.extract_key(res.json(), 'endPoints')
            base_url = url.split('.com')[0] + '.com'
            pagination_end_point = base_url
            pagination_key = "Pagination"
            for end_point in end_points:
                if end_point['type'] == pagination_key:
                    pagination_end_point += end_point['uri'] + '/'
                    break
            return pagination_end_point
        except:
            pass
        return None

    def process_logic(self):
        try:
            isdata = True
            page = 0
            oldurl = ''
            urls = []
            while isdata:
                isloaded, res = self.post_request('https://rapidsos.wd1.myworkdayjobs.com/wday/cxs/rapidsos/RapidSOS/jobs',
                                                  page)
                page = page + 20
                print("collecting page: " + str(page))
                if not isloaded:
                    isdata = False
                    break
                if 'jobPostings' not in res.json(): break
                if len(res.json()['jobPostings']) == 0: break
                objs = res.json()['jobPostings']
                for obj in objs:
                    try:
                        if obj['externalPath'] in urls:
                            isdata = False
                            continue
                        urls.append(obj['externalPath'])
                        jobObj = deepcopy(self.obj)
                        url = 'https://rapidsos.wd1.myworkdayjobs.com/wday/cxs/rapidsos/RapidSOS' + obj['externalPath']
                        jobObj['url'] = 'https://rapidsos.wd1.myworkdayjobs.com/en-US/RapidSOS' + obj['externalPath']
                        try:
                            jobObj['location'] = obj['locationsText']
                        except:
                            jobObj['location'] = 'USA'
                            pass
                        jobObj['title'] = obj['title']
                        isloaded, res = self.get_request(url)
                        if 'jobPostingInfo' in res.json() and isloaded:
                            details = res.json()['jobPostingInfo']
                            jobObj['description'] = details['jobDescription']
                            try:
                                jobObj['location'] = details['location']
                                for loc in details['additionalLocations']:
                                    jobObj['location'] += ', ' + loc
                            except:
                                pass
                        print(jobObj['title'])
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            #print(jobObj['title'])
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