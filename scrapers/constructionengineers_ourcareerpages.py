import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj
import json

# Token
token = 'CONSTRUCTION_ENGINEERS_OUR_CAREER_PAGES'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://constructionengineers.ourcareerpages.com/WebServices/ccp_jobs.aspx?AutoGenerate=yes&GroupBy=&CCPCode=ClearVisionOptical&InAccountID=0&ElementID=BDHRJobListingsCustom&JobOrderBy='

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
        self.domain = 'constructionengineers.com'
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
            # regex = re.compile('.*job-desc-block.*')
            # descs = jobDetail.find_all('div',{'class':regex})
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                jsn = res.text.split('ccpInfo:')[1]
                jsn = jsn.split('}};')[0] + '}'
                jsn = json.loads(jsn)
                if 'CategoryList' not in jsn: return
                for link in jsn['CategoryList']:
                    if 'JobList' not in link: continue
                    for job in link['JobList']:
                        jobObj = deepcopy(self.obj)
                        url = 'https://constructionengineers.ourcareerpages.com/job/' + str(job['ID'])
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        if isloaded:
                            data = BeautifulSoup(jobres.text, 'lxml')
                            jobObj['title'] = data.find_all('h2')[1].text.replace('\n', '').strip()
                            jobObj['location'] = data.find('span', {'class': 'job_location'}).text.split("\xa0")[
                                0].strip()
                            jobObj['description'] = str(data.find('div', {'class': 'nine columns'}))
                        if jobObj['title'] != '' and jobObj['url'] != '':
                            self.allJobs.append(jobObj)
                            print(jobObj)
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
