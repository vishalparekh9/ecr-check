

import json
import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'JOBS_VMWARE_CLOUDHEALTHTECH'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.cloudhealthtech.com'

        self.getHeaders = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': 'searchSource=external; jrasession=fcc9b82a-cb64-44b2-8930-364ad05f27d7; _gcl_au=1.1.1867284864.1650611126; _gid=GA1.2.1763485404.1650611127; _mkto_trk=id:048-SZW-045&token:_mch-vmware.com-1650611126732-50491; _fbp=fb.1.1650611126757.155465246; __adroll_fpc=3351271b2709814aa74d78fc08680018-1650611127223; aam_uuid=61563498918374466282701428247062135372; fs_uid=rs.fullstory.com#16QR4H#6201722340761600:5746972411420672/1682147316; s_tbm1=true; aam_uuid=61563498918374466282701428247062135372; mbox=session#a7368fdaf0e94fcdafadaa909fb7463d#1650613371|PC#a7368fdaf0e94fcdafadaa909fb7463d.31_0#1713856311; RT="z=1&dm=vmware.com&si=88fbae7d-c4b5-4901-973d-a2a407a78461&ss=l2a3cvbv&sl=2&tt=tod&bcn=%2F%2F684d0d43.akstat.io%2F&ld=4bly&ul=5gvn&hd=5gw9"; _ga=GA1.2.427054475.1650611127; _ga_8HN0V85T5P=GS1.1.1650611134.1.1.1650611868.60; i18n=en-US; session_id=e7263455-493b-4219-a52e-eab0a2932e54; jasession=s%3AgYg76YU6MaI6RSNFpfIF7tQvxZ9n-TUd.GOzBV39Dat7hZQ%2Bk8Eop6xRGwTUIWDXsO3uydQKpCmY; _abck=341D96F975EB4A11612D852AB84C9C0B~0~YAAQjvTfF0d3rlKAAQAAEzLbVAcz67L8Od7g8k1vN4t2o+MS0jZmmHP8XOqrmSHbFETRA4S1zunyrbISBO+UJ2TrSP5A5hy6QwQTbzU+a2WCf1VYqTXpLK+o1oxfFyvojwU69y8J3rhpTJ8V7E9SykYw0fI44IkCdDPHTYJMKYPeyu+JHqgEyoLDs/+vtZ98A4CiXvbfDzCVzbXrrIWif7eEtrsmpJI8d9vQ9avKhtb1RtOI6rywlOUErXVPph0pePxDh8zM2yOg4tgkr6TCt+r8A4vr/isRTbdGW+D+2FeeIzxUxFrq+AmoMgURuazVNf9sv0jVvtZm3YCtxPbLdoo0CkQkXSwRJ4cpP42BVM0O69prJCgcdw2iyqxD2A==~-1~-1~-1; AMCV_5B29123F5245AD520A490D45%40AdobeOrg=-1124106680%7CMCIDTS%7C19105%7CMCMID%7C69113626973650338253456740274425829577%7CMCAAMLH-1651295894%7C12%7CMCAAMB-1651295894%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1650698294s%7CNONE%7CvVersion%7C5.2.0; AMCVS_5B29123F5245AD520A490D45%40AdobeOrg=1; s_cc=true; s_tbm=true; _janalytics_ses.eab2=*; _uetvid=963db1c0c20a11ec9c596de783d0f459; _uetsid=963d6b70c20a11ecbcea295e3fa68bb4; __ar_v4=OSU6T4K5BNEFDBKAQHSKNI%3A20220422%3A13%7C3T3E3J57XBHLNN2SF6MDM3%3A20220422%3A13%7C4RMH4B3GVNF6PPORXRHP7H%3A20220422%3A13; _janalytics_id.eab2=99bff33b-b15f-4a3d-a194-45ded9be34f9.1650550540.3.1650691151.1650612041.b45cec11-5f05-4d3e-9c39-c9c85930a4bb; s_tp=6865; s_ppv=vmware%2520%253A%2520careers%2520%253A%2520main%2520%253A%2520jobs%2C25%2C19%2C1720; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Apr+23+2022+10%3A50%3A39+GMT%2B0530+(India+Standard+Time)&version=6.31.0&isIABGlobal=false&hosts=&consentId=e229105f-a58a-476d-9ff8-112acfd25569&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&AwaitingReconsent=false; utag_main=v_id:01805016dcc90018cb524d043b0b05074002006c00bb3$_sn:2$_ss:0$_st:1650693039286$_pn:3%3Bexp-session$ses_id:1650691093453%3Bexp-session',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'cloudhealthtech.com'
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
            page = 0
            isPage = True
            while isPage:
                page = page + 1
                print("Collecting for page ", page)
                url = f'https://careers.vmware.com/api/jobs?keywords=CloudHealth&limit=25&page={page}&sortBy=relevance&descending=false&internal=false'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    try:
                        data = res.json()['jobs']
                        if len(data) > 0:
                            for rd in data:
                                jobObj = deepcopy(self.obj)
                                jobObj['title'] = rd['data']['title']
                                jobObj['location'] = rd['data']['full_location']
                                url = str(rd['data']['apply_url']).replace("/apply", "")
                                jobObj['url'] = url
                                isloaded, jobres = self.get_request(url.replace("https://vmware.wd1.myworkdayjobs.com/VMware/", "https://vmware.wd1.myworkdayjobs.com/wday/cxs/vmware/VMware/"))
                                if isloaded:
                                    try:
                                        jobData = jobres.json()['jobPostingInfo']
                                        jd = jobData['jobDescription']
                                        jobObj['description'] = str(jd)
                                        if jobObj['title'] != '' and jobObj['url'] != '':
                                            self.allJobs.append(jobObj)
                                            print(jobObj)
                                    except Exception as e:
                                        print(e)
                                        pass
                        else:
                            print("Job Not Found")
                            isPage = False
                            break
                    except Exception as e:
                        pass
            else:
                print("Job Not Found")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))