import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'JOBSUSA_1800_CAREERS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.1800jobsusa.com/'

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
        self.domain = '1800jobsusa.com'
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
            page = -10
            isPage = True
            while isPage:
                page = page + 10
                url = f'https://1800jobsusa.com/api/jobs?empty=empty&&draw=2&columns[0][data]=name&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=category&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=city&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=state&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=country&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start={page}&length=10&search[value]=&search[regex]=false'
                isloaded, res = self.get_request(url)
                if isloaded:
                    if len(res.json()["data"]) > 0:
                        for data in res.json()["data"]:
                            if data:
                                jobObj = deepcopy(self.obj)
                                url = data['url']
                                jobObj['url'] = url
                                jobObj['title'] = data['name']
                                jobObj['location'] = data['location']
                                jobObj['description'] = data['description']
                                if jobObj['title'] != '' and jobObj['url'] != '' and len(jobObj['description']) > 255:
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        isPage = False
                        break
                else:
                    print("Job Not Found")
            else:
                print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
