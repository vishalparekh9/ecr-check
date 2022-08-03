import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'WHITEJACOBS_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://whitejacobs.com'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.session = requests.session()
        self.domain = 'whitejacobs.com'
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
            page = -50
            isPage = True
            while isPage:
                page = page + 50
                url = f'https://api.jobsearcher.com/v1/jobs?status=all&exactCompany%5Bmust%5D=White%2C%20Jacobs%20%26%20Associates&type=organic&limit=50&offset={page}&distance=25&sortBy%5B0%5D=updatedDate&sortOrder%5B0%5D=desc&ignoreScore=true'
                isloaded, res = self.get_request(url)
                if isloaded:
                    links = res.json()['data']
                    if len(links) > 0:
                        for link in links:
                            if 'originalDescription' in link:
                                jobObj = deepcopy(self.obj)
                                url = "https://jobsearcher.com" + link['jsUrl']
                                jobObj['url'] = url
                                jobObj['title'] = link['title'].strip()
                                jobObj['location'] = link['location']['city'] + ", " + link['location']['state']
                                jobObj['description'] = link['originalDescription']
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
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
