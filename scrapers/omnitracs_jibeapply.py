import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'OMNITRACS_JIBEAPPLY_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://omnitracs.jibeapply.com/working-here/jobs'

        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Content-Type': 'application/json; charset=utf-8'
        }
        self.session = requests.session()
        self.domain = 'omnitracs.com'
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
            jobid = ""
            url = 'https://omnitracs.jibeapply.com/api/jobs?page=1'
            isloaded, res = self.get_request(url)
            if isloaded:
                pages = res.json()['totalCount']
                isdata = True
                for page in range(1, pages):
                    url = f'https://omnitracs.jibeapply.com/api/jobs?page={page}'
                    print("Collecting for page : ", page)

                    # page = page + 1

                    isloaded, res = self.get_request(url)
                    if isloaded:
                        for data in res.json()['jobs']:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = data['data']['apply_url']
                            jobObj['title'] = data['data']['title'].replace('\n', '').replace('\r', '').strip()
                            jobObj['location'] = data['data']['location_name'].replace('\n', '').replace('\r', '').strip()
                            jobObj['description'] = str(data['data']['description'])
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)

                    else:
                        print("Job not Found!")
                        isdata = False

                else:
                    isdata = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
