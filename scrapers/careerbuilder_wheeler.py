import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup
import json
import re
import os
import common as cf
# Token
token = 'CAREERBUILDER_WHEELER'


class CRAWLER(object):
    def __init__(self):
        self.location = 'wheeler'.replace(' ', '+')
        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            #'x-csrf-token': 'ru/YN/flQbI3SCMLGDozCVvu8G8oEMKxxC/yLLei5NZ4EqeTeaDCLHGvenC3P4Cs+878rLBbwUGcesN/5sa/ZQ==',
            #'x-newrelic-id': 'VgYHUVdbDhACUFlXAwYPX1U=',
            #'x-requested-with': 'XMLHttpRequest'
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
        self.domain = 'careerbuilder.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def html_request(self, url):
        try:
            res = self.session.get(url, headers=self.htmlHeaders)
            return True, res
        except Exception as e:
            print(e)
        return False, False
    def get_request(self, url):
        try:
            res = self.session.get(url, headers=self.getHeaders)
            return True, res
        except Exception as e:
            print(e)
        return False, False

    def get_location(self):
        try:
            res = self.session.get('https://www.careerbuilder.com/autocomplete/location/?term=' + str(self.location.replace('+', ' ')), headers=self.getHeaders)
            return True, res
        except Exception as e:
            print(e)
        return False, False
    def scrapDomain(self, company, domains):
        try:
            newUrl = str("https://www.careerbuilder.com/company/" + str(company).replace(" ", "-").lower() + "/" + domains + ".js?co_overview=true")
            isloaded, res = self.get_request(newUrl)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                link = data.find("div", {"class": "contact-us-link"}).find("a").get("href")
                link = link.lower().replace('http://','').replace('https://','').replace('www.','')
                link = link.split('?')[0]
                link = link.split('/')[0]
                return link
        except (AttributeError, KeyError, Exception, ValueError) as e:
            pass
        return 'careerbuilder.com'


    def get_page_details(self, links):
        try:
            self.allJobs = []
            for link in links:
                jobObj = deepcopy(self.obj)
                regex = re.compile('.*/job/.*')
                try:
                    findDomain = link.find("a").get("data-company-did")
                    jobObj['title'] = link.find("div", {"class": "data-results-title dark-blue-text b"}).text
                    url = str("https://www.careerbuilder.com" + link.find("a",{'href':regex}).get("href"))
                    jobObj['url'] = url
                    jobObj['company'] = link.find("div", {"class": "data-details"}).find_all("span")[0].text.strip()
                    jobObj['location'] = link.find("div", {"class": "data-details"}).find_all("span")[1].text.strip() + ', United States'
                    jobObj['domain'] = 'careerbuilder.com'
                    link = cf.domain_finder(jobObj['company'])
                    if link: jobObj['domain'] = link
                    try:
                        isloaded, res = self.html_request(url)
                        if isloaded:
                            jobData = BeautifulSoup(res.text, "lxml")
                            jobObj['description'] = str(jobData.find('div',{'id':'jdp_description'}))
                    except:
                        pass
                    if findDomain == '' and jobObj['domain'] == 'careerbuilder.com':
                        jobObj['domain'] = self.scrapDomain(jobObj['company'], findDomain.strip())
                    print(jobObj['domain'])
                    if jobObj['title'] != '' and jobObj['url'] != '':
                        self.allJobs.append(jobObj)
                except:
                    pass
        except Exception as e:
            print(e)
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
    def process_logic(self):
        try:
            self.baseUrl = 'https://www.careerbuilder.com/'
            isloaded, res = self.html_request(self.baseUrl)
            soup = BeautifulSoup(res.text, "lxml")
            #if 'xpid:' not in res.text: return
            #token = soup.find('meta',{'name':'csrf-token'}).get('content')
            #xpid = res.text.split('xpid:')[1].split(',')[0].replace('"','')
            #self.getHeaders['x-newrelic-id'] = xpid
            #self.getHeaders['x-csrf-token'] = token
            isloaded, location = self.get_location()
            locations  = [loc for loc in location.json() if self.location.lower().replace('+', ' ') in loc.lower()]
            keywords = self.read_keywords()
            for loc in locations[:2]:
                for key in keywords:
                    print("Collecting jobs for: " + str(key))
                    self.search = key.strip().replace(' ', '+')
                    page = 0
                    isPage = True
                    while isPage:
                        page = page + 1
                        print("Collecting for page ", page)
                        url = 'https://www.careerbuilder.com/jobs.js?keywords='+self.search+'&location='+loc+'&cb_workhome=false&country_code=US&posted=1&pay=&radius=30&page_number='+str(page)+''
                        isloaded, res = self.get_request(url)
                        if isloaded:
                            try:
                                searchPattern = re.search(r"\.append\(\"(.*?)\"\)", res.text)
                                htmlData = searchPattern.group()
                                htmlData2 = str(htmlData).replace("\\'", "'").replace('\\"', '"').replace("\\n", "").replace("\\/", "/").strip()
                                data = BeautifulSoup(htmlData2, "lxml")
                                links = data.find_all("li")
                                if len(links)> 0:
                                    self.get_page_details(links)
                                    print(len(self.allJobs))
                                    cf.insert_rows(self.allJobs, self.site, self.iserror, self.domain, False)
                                else:
                                    print("Job Not Found")
                                    ispage = False
                                    break
                            except Exception as e:
                                print(e)
                                ispage = False
                        else:
                            print("Job Not Found")
                            ispage = False
                            break
                    

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))