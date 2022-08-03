import requests
from copy import deepcopy
import json
from index import get_obj

token = 'MYWORKDAYSJOB_BANNERHEALTH'
class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://bannerhealth.wd5.myworkdayjobs.com/Careers'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'application/json,application/xml',
        }
        self.session = requests.session()
        self.domain = 'bannerhealth.com'
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
    
    def extract_key(self,elem, key):
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
            isloaded, res = self.get_request(self.baseUrl)
            
            pagination_end_point = self.get_page_URL(res, self.baseUrl)
            isdata = True
            page = 0
            if pagination_end_point == None: return 
            while isdata and pagination_end_point:
                url = pagination_end_point+str(page)
                print("Collecting page: " + str(page))
                isloaded, res = self.get_request(url)
                if isloaded:
                    page = page + 50
                    if res.text == '': break
                    if 'body' not in res.json(): break
                    if 'children' not in res.json()['body']: break
                    if len(res.json()['body']['children']) == 0: break
                    if 'children' not in res.json()['body']['children'][0]: break
                    if len(res.json()['body']['children'][0]['children']) == 0: break
                    if 'listItems' in res.json()['body']['children'][0]['children'][0]:
                        lis = res.json()['body']['children'][0]['children'][0]['listItems']
                        if len(lis) == 0:
                            isdata=False
                            break
                        for link in lis:
                            a = link['title']['commandLink']
                            if a == None:
                                isdata = False
                                break
                            jobObj = deepcopy(self.obj)
                            url = 'https://'+ pagination_end_point.split('/')[2] + a
                            jobObj['url'] = url
                            try:
                                host = pagination_end_point.split('/')[2]
                                code = host.split('.')[0]
                                url1 = a.lower().replace('/en-us/','/')
                                url1 = 'https://'+ host + '/wday/cxs/' + code + url1
                                isloaded, jobres = self.get_request(url1)
                                jobObj['title'] = link['title']['instances'][0]['text']
                                jobObj['title'] = jobres.json()['jobPostingInfo']['title']
                                jobObj['description'] = jobres.json()['jobPostingInfo']['jobDescription']
                                jobObj['location'] = jobres.json()['jobPostingInfo']['location']
                                if 'additionalLocations' in jobres.json()['jobPostingInfo']:
                                    for loc in jobres.json()['jobPostingInfo']['additionalLocations']:
                                        jobObj['location'] += ', ' + str(loc)
                                print(jobObj['location'])
                            except Exception as e:
                                print(e)
                            if jobObj['description'] == "":
                                try:
                                    isloaded, jobres = self.get_request(url)
                                    jobObj['title'] = link['title']['instances'][0]['text']
                                    jobObj['description'] = json.loads(jobres.json()['structuredDataAttributes']['data'])['description']
                                    if 'children' in jobres.json()['body']:
                                        c = 0
                                        for child1 in jobres.json()['body']['children']:
                                            if 'children' in child1:
                                                for child2 in child1['children']:
                                                    if 'children' in child2:
                                                        child3= child2['children']
                                                        for loc in child3:
                                                            if 'iconName' in loc:
                                                                if loc['iconName'].lower() == 'LOCATION'.lower():
                                                                    if c == 0:
                                                                        jobObj['location'] += loc['imageLabel']
                                                                    else:
                                                                        jobObj['location'] += ' | ' + loc['imageLabel']
                                                                    c = c + 1
                                except Exception as e:
                                    pass
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                    else:
                        isdata = False
                        print('No Job Data Found!')
                else:
                    isdata = False
        except Exception as e:
            print(e)
            self.iserror = True
            isdata = False

if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))