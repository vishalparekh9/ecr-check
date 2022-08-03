import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'GRAY_SHIFT_RECRUITER_BOX_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://app.recruiterbox.com/widget/84528/openings/'

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
        self.domain = 'grayshift.com'
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
                data = res.json()
                for jobData in data:
                    jobObj = deepcopy(self.obj)
                    url = 'https://app.recruiterbox.com/widget/84528/openings/' + str(jobData['id'])
                    jobObj['url'] = url
                    jobObj['title'] = jobData['title']
                    jobObj['location'] = str(jobData['location']['city'] + ", United States")
                    jobObj['description'] = jobData['description']

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