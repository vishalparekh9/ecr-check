import requests
from copy import deepcopy
from index import get_obj
from bs4 import BeautifulSoup

# Token
token = 'GILEAD_YELLO_CAREER_JOBS'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://www.gilead.com'

        self.getHeaders = {
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }

        self.session = requests.session()
        self.domain = 'ey.com'
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
            page = 0
            isPage = True
            while isPage:
                page = page + 1
                print("Collecting for page ", page)
                url = f'https://gilead.yello.co/job_boards/v42vD4vKxb3AkKvV93YsrQ/search?query=&filters=&page_number={page}&job_board_tab_identifier=e450ef63-65d7-0578-dd52-0d771df5cc5d'
                print(url)
                isloaded, res = self.get_request(url)
                if isloaded:
                    # htmlData2 = str(htmlData).replace("\\'", "'").replace('\\"', '"').replace("\\n", "").replace("\\/", "/").strip()

                    data = BeautifulSoup(str(res.json()['html']), "lxml")
                    if data:
                        links = data.find_all("li", {"class": "search-results__item"})
                        if links is not None:
                            for link in links:
                                jobObj = deepcopy(self.obj)
                                jobObj['title'] = link.find("a").text
                                url = str("https://gilead.yello.co" + link.find("a").get("href"))
                                jobObj['url'] = url
                                jobObj['location'] = str("United States")

                                isloaded, res = self.get_request(url)
                                if isloaded:
                                    jobData = BeautifulSoup(res.text, "lxml")
                                    jobDesc = jobData.find("section", {"class": "job-details__description pull-left"})
                                    jobObj['description'] = str(jobDesc)
                                    if jobObj['title'] != '' and jobObj['url'] != '':
                                        self.allJobs.append(jobObj)
                                        print(jobObj)

                        else:
                            print("Job Not Found")
                            ispage = False
                            break
                    else:
                        print("Job Not Found")
                        ispage = False
                        break
            else:
                print("Job Not Found")
                ispage = False

        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
