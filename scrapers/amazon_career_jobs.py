import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'AMAZON_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://amazon.jobs'

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
        self.domain = 'amazon.com'
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
            page = -100
            isPage = True
            while isPage:
                page = page + 100
                print(f"Collecting for page {page}")
                url = f'https://amazon.jobs/en-gb/search.json?radius=24km&facets[]=normalized_country_code&facets[]=normalized_state_name&facets[]=normalized_city_name&facets[]=location&facets[]=business_category&facets[]=category&facets[]=schedule_type_id&facets[]=employee_class&facets[]=normalized_location&facets[]=job_function_id&facets[]=is_manager&facets[]=is_intern&offset={page}&result_limit=100&sort=relevant&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&category[]=software-development&'
                isloaded, res = self.get_request(url)
                if isloaded:
                    if len(res.json()['jobs']) > 0:
                        for li in res.json()['jobs']:
                            jobObj = deepcopy(self.obj)
                            jobObj['url'] = 'https://amazon.jobs' + str(li['job_path'])
                            jobObj['title'] = li['title']
                            jobObj['location'] = str(li['location'])
                            if li["description"] is not None and li["preferred_qualifications"] is not None and li["basic_qualifications"] is not None:
                                jobObj['description'] = str(li['description'] + "<br />" + li['preferred_qualifications'] + "<br />" + li['basic_qualifications'])

                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        break
            else:
                print('No Job Data Found!')
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))