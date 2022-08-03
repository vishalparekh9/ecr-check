
import json
import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'JOB_APP_NETWORK_SCOOTERSCOFFEE_COM'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://apply.jobappnetwork.com/scooters-coffee'

        self.getHeaders = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '355',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
        }
        self.session = requests.session()
        self.domain = 'scooterscoffee.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False

    def post_request(self, url, payload):
        try:
            res = self.session.request("POST", url=url, headers=self.getHeaders, data=payload)
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
                url = 'https://prod-kong.internal.talentreef.com/apply/proxy-es/search-en-us/posting/_search'

                payload = '{"from":'+str(page)+',"size":10,"_source":["positionType","category","socialRecruitingAttribute1","description","address","jobId","clientId","clientName","brandId","location","internalOrExternal","url"],"query":{"bool":{"filter":[{"terms":{"clientId.raw":["17560","17565","17548","17584","17540","17581","17521","17518","17537","17522","17549","17547","17578","17534","17573","17580","17524","17572","17538","17542","17571","17564","17569","17576","17546","17585","17545","17528","17588","17491","17579","17591","17590","17554","17535","17523","17544","17562","17589","17529","17527","17566","17593","17536","17517","17526","17568","17543","17563","17530","17558","17575","17592","17552","17557","17533","17525","17567","17570","17583","17824","17551","17553","17520","17486","17550","17582","17586","17556","17559","17574","17519","17561","17046","17577","17587","17555","17539","17541","18602","18773","19223","19273","19306","19395","19413","19432","19442","19431","19588","19586","19628","19653","19655","19621","19691","19695","19711","19709","19710","19732","19749","19748","19755","19788","19790","19791","19805","19835","19855","19856","19885","19886","19926","19915","19978","19977","19986","19984","19983","20006","20032","20031","20040","20039","20051","20085","19351","20149","20147","20145","20146","20152","20166","20161","20164","20202","20203","20259","20290","20319","20318","20335","20334","20333","20410","20409","20407","20408","20482","20490","20488","20484","20489","20485","20508","20515","20516","20514","19989","20532","20543","20593","20618","20615","20617","20616","20614","20652","20658","20722","20727","20740","20738","20741","20744","20742","20739","20819","20818","20838","20837","20836","20874","20873","20886","20916","20917","20918","20915","20928","20927","20949","20948","20950","20977","20980","20978","20976","20979","20981","20994","21009","21034"]}},{"terms":{"brand.raw":["Scooters Coffee"]}},{"terms":{"internalOrExternal":[{"internalOrExternal":"externalOnly"}]}}]}},"sort":[{"positionType.raw":{"order":"asc"}}]}'
                isloaded, res = self.post_request(url, payload=payload)
                if isloaded:
                    links = json.loads(res.text)['hits']['hits']
                    if len(links) > 0:
                        for link in links:
                            jobObj = deepcopy(self.obj)
                            clientId = link['_source']['clientId']
                            jobId = link['_source']['jobId']
                            url = f"https://apply.jobappnetwork.com/clients/{clientId}/posting/{jobId}/en"
                            jobObj['url'] = url
                            jobObj['title'] = link['_source']['positionType']
                            jobObj['location'] = link['_source']['address']['city']
                            jobObj['description'] = str(link['_source']['description'])
                            if len(jobObj['description']) > 100:
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                    else:
                        isPage = False
                        break
                else:
                    print("Job Not Found")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))