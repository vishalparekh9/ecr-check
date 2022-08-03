import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from index import get_obj

# Token
token = 'TEGNA_10TV_COLUMBUS_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://tegna.jobs.net/jobs?keywords=&location=Columbus'

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
        self.domain = '10tv.com'
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
                data = BeautifulSoup(res.text, 'lxml')
                jobList = data.find_all('li', {'class': 'data-results-content-parent'})

                if jobList:
                    for job in jobList:
                        jobObj = deepcopy(self.obj)
                        url = job.find('a').get('href')
                        url = "https://tegna.jobs.net" + url
                        jobObj['url'] = url
                        isloaded, jobres = self.get_request(url)
                        jobDetail = BeautifulSoup(jobres.text, 'lxml')
                        if isloaded:
                            headerInfo = jobDetail.find('div', {'class': 'data-display-header_info-content'})
                            dataDetails = headerInfo.find('div', {'class': 'data-details'}).find_all('span')
                            location = dataDetails[1].text.strip()
                            jobObj['title'] = jobDetail.find('h2', {'class': 'jdp_title_header'}).text.strip()
                            jobObj['location'] = location
                            jobDescription = jobDetail.find('div', {'id': 'jdp_description'}).text
                            companyOverview = jobDetail.find('div', {'id': 'jdp_company'})
                            jobObj['description'] += str(jobDescription)
                            jobObj['description'] += str(companyOverview)
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                else:
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))