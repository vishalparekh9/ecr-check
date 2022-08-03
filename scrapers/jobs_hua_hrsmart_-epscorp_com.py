
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'JOBS_HUA_HRSMART_EPSCORP'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://epscorp.hua.hrsmart.com'
        self.session = requests.session()
        self.domain = 'epscorp.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def get_request(self, url):
        try:
            getHeaders = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
                'Accept':
                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            }
            res = self.session.get(url, headers=getHeaders)
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
                isloaded, res = self.get_request(
                    f"https://epscorp.hua.hrsmart.com/hr/ats/JobSearch/viewAll/jobSearchPaginationExternal_pageSize:100/jobSearchPaginationExternal_page:{page}")
                if isloaded:
                    data = BeautifulSoup(res.text, 'lxml')
                    jobDataChunk = data.find('tbody')
                    if jobDataChunk is not None:
                        aTag = jobDataChunk.find_all('tr')
                        if len(aTag) > 1:
                            for link in aTag:
                                jobObj = deepcopy(self.obj)
                                url = 'https://epscorp.hua.hrsmart.com' + link.find_all("td")[0].find("a").get("href")
                                jobObj['url'] = url
                                jobObj['title'] = str(link.find('span').text.strip())
                                jobObj['location'] = str(link.find_all("td")[1].text.strip())
                                isloaded, resJobData = self.get_request(url)
                                if isloaded:
                                    jobDetails = BeautifulSoup(resJobData.text, 'lxml')
                                    jobObj['description'] = str(jobDetails.find('div', {'id': 'job-detail'}))
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)
                        else:
                            isPage = False
                            break
                    else:
                        print('No Job Data Found!')
                        isPage = False
                        break
                else:
                    print('No Job Data Found!')
                    
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))