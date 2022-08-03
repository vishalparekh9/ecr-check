
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'INDOVANCE_ZOHO_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://indovance.zohorecruit.com/careers'

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
        self.domain = 'indovance.com'
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
            isloaded, res = self.get_request(self.baseUrl)
            if isloaded:
                data = BeautifulSoup(res.text, "lxml")
                links = data.find_all('tr', {"class": "jobDetailRow"})
                for link in links:
                    jobObj = deepcopy(self.obj)
                    url = "https://indovance.zohorecruit.com" + str(link.find("a", {"class": "jobdetail"}).get("href"))
                    jobObj['url'] = url
                    jobObj['title'] = link.find_all("td")[1].text
                    jobObj['location'] = str(link.find_all("td")[3].text) + ", " + str(link.find_all("td")[4].text)
                    if jobObj['location'] == ", ":
                        jobObj['location'] = "United States"
                    isloaded, jobRes = self.get_request(url.replace('iframe=true', 'iframe=false'))
                    if isloaded:
                        jobDesc = jobRes.json()['jobDescriptionDetails'][0]['richText']['value']
                        jobObj['description'] = str(jobDesc)
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