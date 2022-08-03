import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'WIPRO_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://careers.wipro.com/api/jobs?location=United%2520States&woe=12&stretchUnit=MILES&stretch=0&sortBy=posted_date&descending=true&internal=false&limit=100&page='

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
        self.domain = 'wipro.com'
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
            isdata = True
            page = 1
            while isdata:
                print("Collecting page: " + str(page))
                url = self.baseUrl + str(page)
                page = page + 1
                isloaded, res = self.get_request(url)
                if 'jobs' not in res.json(): break
                if len(res.json()['jobs']) == 0: break
                links = res.json()['jobs']
                if links:
                    for link in links:
                        try:
                            link = link['data']
                            jobObj = deepcopy(self.obj)
                            url = 'https://careers.wipro.com/opportunities/jobs/' + str(link['slug'])
                            jobObj['url'] = url
                            jobObj['title'] = link['title']
                            if 'city' in link:
                                jobObj['location'] = link['city']
                            if 'state' in link:
                                jobObj['location'] += ', ' + link['state']
                            isloaded, jobres = self.get_request(
                                'https://careers.wipro.com/api/jobs/' + str(link['slug']))
                            if isloaded:
                                jobObj['description'] = jobres.json()['description']
                            if jobObj['title'] != '' and jobObj['url'] != '':
                                self.allJobs.append(jobObj)
                                print(jobObj)
                        except:
                            pass
                else:
                    isdata = False
                    print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))