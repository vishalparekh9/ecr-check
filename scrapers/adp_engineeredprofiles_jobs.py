from pydoc import isdata
import requests
from copy import deepcopy
from index import get_obj

#Token
token = 'ADP_ENGINEEREDPROFILES_JOBS'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = ''

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'engineeredprofiles.com'
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
            jobid = ""
            cid = '92bb3c10-a886-4ab7-a3f5-3bcc40188e49'
            icids = '19000101_000001'
            page = 1
            isdata = True
            while isdata:
                print("collecting data from: " + str(page))
                url = 'https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions?cid='+str(cid)+'&timeStamp=1646215364762&lang=en_US&ccId='+str(icids)+'&locale=en_US&$top=20&$skip=' + str(page)
                page = page + 20
                isloaded, res = self.get_request(url)
                if isloaded:
                    if 'jobRequisitions' not in res.json(): break
                    if len(res.json()['jobRequisitions']) == 0: break
                    for data in res.json()['jobRequisitions']:
                        position_id = data['itemID']
                        jobObj = deepcopy(self.obj)
                        jobObj['title'] = data['requisitionTitle']
                        # print(data['postDate'])
                        try:
                            jobObj['location'] = data['requisitionLocations'][0]['nameCode']['shortName']
                            jobid = data['customFieldGroup']['stringFields'][0]['stringValue']
                        except IndexError:
                            jobObj['location'] = 'United States'

                        url = 'https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions/'+str(position_id)+'?cid='+str(cid)+'&timeStamp=1646215302900&lang=en_US&ccId='+str(icids)+'&locale=en_US'
                        jobObj['url'] = url

                        isloaded, res = self.get_request(url)
                        if isloaded:
                            jobObj['description'] = str(res.json()['requisitionDescription'])
                            jobObj['url'] = "https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid="+str(cid)+"&ccId="+str(icids)+"&jobId="+str(jobid)+"&lang=en_US&source=LI"
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                else:
                    print("Job Not Found")
                    isdata = False
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))