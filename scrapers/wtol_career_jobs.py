import re
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'WTOL_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://wtol.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'wtol.com'
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

    def scrapDomain(self, company, domains):
        fetchedDomain = None
        try:
            newUrl = str("https://www.careerbuilder.com/company/" + str(company).replace(" ", "-").lower() + "/" + domains + ".js?co_overview=true")
            isloaded, res = self.get_request(newUrl)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find("div", {"class": "contact-us-link"}).find("a").get("href")
                if links:
                    fetchedDomain = links
        except (AttributeError, KeyError, Exception, ValueError) as e:
            pass
        return fetchedDomain

    def process_logic(self):
        try:
            page = 0
            isPage = True
            while isPage:
                page = page + 1
                url = f'https://tegna.jobs.net/jobs.js?keywords=&location=United+States&page_number={page}'
                isloaded, res = self.get_request(url)
                if isloaded:
                    searchPattern = re.search(r"\.append\(\"(.*?)\"\);", res.text)
                    htmlData = searchPattern.group()
                    htmlData2 = str(htmlData).replace("\\'", "'").replace('\\"', '"').replace("\\n", "").replace("\\/", "/").strip()
                    data = BeautifulSoup(htmlData2, "lxml")
                    if data:
                        links = data.find_all("li", {"class": "data-results-content-parent relative"})
                        if links is not None and len(links) > 0:
                            for link in links:
                                jobObj = deepcopy(self.obj)
                                if link.find("a").get("data-company-did") != "":
                                    findDomain = link.find("a").get("data-company-did")
                                    jobObj['title'] = link.find("div", {"class": "data-results-title dark-blue-text b"}).text
                                    url = str("https://tegna.jobs.net/job" + link.find("a").get("href"))
                                    jobObj['url'] = url
                                    jobObj['company'] = str(link.find("div", {"class": "data-details"}).find_all("span")[0].text)
                                    jobObj['location'] = str(link.find("div", {"class": "data-details"}).find_all("span")[1].text)
                                    isloaded, res = self.get_request(url)
                                    if isloaded:
                                        jobData = BeautifulSoup(res.text, "lxml")
                                        jobDesc = jobData.find("div", {"class": "col big col-mobile-full jdp-left-content"})
                                        try:
                                            jobObj['description'] = str(jobDesc)
                                            Domains = self.scrapDomain(str(jobObj['company']).strip(), findDomain.strip())
                                            jobObj['domain'] = Domains.replace("https://www.", "").replace(
                                                "http://www.", "").replace("https://tegna.", "").replace(
                                                "www.", "").replace("/", "").replace("us-en", "").strip()

                                            if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['domain'] != '':
                                                self.allJobs.append(jobObj)
                                                print(jobObj)
                                        except (AttributeError, KeyError, Exception, ValueError) as e:
                                            pass
                        else:
                            print("Job not Found!")
                            isPage = False
                            break
                else:
                    print("Job not Found!")
                    isPage = False
            else:
                print("Job not Found!")

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
