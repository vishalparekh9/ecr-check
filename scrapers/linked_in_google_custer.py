import os
import time
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj
import common as cf

# Token
token = 'LINKED_IN_GOOGLE_CUSTER'


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
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }
        self.session = requests.session()
        self.domain = 'googlejobs.com'
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

    def process_logic(self):
        try:
            page = 0
            isPage = True
            islinked_in = True
            while isPage:
                page += 10
                time.sleep(0.5)
                job_keywords = self.read_keywords()
                if job_keywords:
                    for keyword in job_keywords:
                        keyword = keyword.strip().replace(" ", "+").replace("\n", "").replace("\r", "")
                        companyLocations = 'custer'
                        via = ''
                        if islinked_in:
                            source = 'linkedin'
                            via = f'+via:+{source}'.replace(" ", "+").replace("\n", "").replace("\r", "")
                            print(via)

                        url = f"https://www.google.com/search?vet=&ei=&rlz=&yv=3&rciv=jb&nfpr=0&chips=date_posted:week,employment_type:FULLTIME&schips=date_posted;week,employment_type;FULLTIME&q={keyword}+jobs{via}+location:+{companyLocations}&start={page}&asearch=jb_list&cs=1&async=_id:VoQFxe,_pms:hts,_fmt:pc&lrad=100.0"
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            soup = BeautifulSoup(res.text, 'lxml')
                            links = soup.find_all('li', {'class': 'iFjolb gws-plugins-horizon-jobs__li-ed'})
                            if len(links) > 1:
                                for link in links:
                                    try:
                                        jobObj = deepcopy(self.obj)
                                        jobObj['title'] = link.find('div', {'class': 'BjJfJf PUpOsf'}).text.replace(',', ' - ').replace('\n', '').replace('\r', '')
                                        jobObj['company'] = link.find('div', {'class': "vNEEBe"}).text.replace(',', ' - ').replace('\n', '').replace('\r', '')
                                        jobObj['location'] = link.find('div', {'class': "Qk80Jf"}).text.replace(',', ' - ').replace('\n', '').replace('\r', '')
                                        jobObj['description'] = str(link.find('div', {'class': 'YgLbBe'})).replace(',', ' - ').replace('\n', '').replace('\r', '')
                                        jobObj['url'] = link.find('a', {'class': "pMhGee Co68jc j0vryd"})['href']
                                        if "?" in jobObj['url']:
                                            jobObj['url'] = str(jobObj['url']).split("?")[0]
                                        link_domains = cf.domain_finder(jobObj['company'])
                                        jobObj['domain'] = self.domain
                                        if link_domains: jobObj['domain'] = link_domains
                                    except:
                                        pass

                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj['title'])
                                cf.insert_rows(self.allJobs, self.site, self.iserror, self.domain, False)
                                self.allJobs = []
                            else:
                                if islinked_in:
                                    print('No Job Data Found in Linkedin!')
                                    islinked_in = False
                                    page = 0
                                    print("*"*100)
                                else:
                                    print('No Job Data Found!')
                                    isPage = False
                                    break

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))