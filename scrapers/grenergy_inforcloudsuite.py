import requests
from copy import deepcopy
from index import get_obj

# Token
token = 'INFORCLOUDSUITE_GRENERGY'


class CRAWLER(object):
    def __init__(self):
        self.baseUrl = 'https://css-grenergy-prd.inforcloudsuite.com/hcm/CandidateSelfService/controller.servlet?dataarea=hcm&context.session.key.JobBoard=EXTERNAL&context.session.key.HROrganization=1'

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
        self.domain = 'greatriverenergy.com'
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
            url = f'https://css-grenergy-prd.inforcloudsuite.com/hcm/soapExt/ldrest/JobPosting/JobPostingListWebServices_ListOperation?_clientType=INTERNAL&JobBoard=EXTERNAL&LocationOfJob=+&Category=+&SubCategory=+&WorkType=+&JobRequisition=+&__Description_translation___=+&JobPosting=+&PostingStatus=2&PostingDateRange.Begin=+&PostingDateRange.End=+&JobRequisitionPriority=+&csk.IsoLocale=en&HROrganization=1&_limit=-1&AtApplicationLimit=+&_=1650210261136'
            print(url)
            isloaded, res = self.get_request(url)
            if isloaded:
                data = res.json()['JobPostingListWebServices_ListOperationResponseArray']
                if len(data) > 0:
                    for link in data:
                        try:
                            jobObj = deepcopy(self.obj)
                            jobId = link['JobPostingListWebServices_ListOperationResponse']['JobRequisition']
                            url = str(
                                f"https://css-grenergy-prd.inforcloudsuite.com/hcm/soapExt/ldrest/JobPosting/Find_PostingDisplay_FormOperation?JobPosting=1&JobRequisition={jobId}&Description=+&__Description_translation___=+&PositionDescription=+&__PositionDescription_translation___=+&LocationOfJob.Description=+&__LocationOfJob.Description_translation___=+&Category.Description=+&RelationshipToOrganization.Description=+&PostingDateRange.Begin=+&PostingDateRange.End=+&SalaryRangeAmount=+&SalaryRange.BeginningPay=+&SalaryRange.EndingPay=+&SalaryEntered=+&StatusSwitchForCandidateSpace=+&SalaryRange.PayRangeCurrencyCode=+&Live=+&JobRequisitionLocation=+&JobRequisitionConsentAgreement=+&JobRequisitionAcknowledgement=+&JobRequisitionSelfIdConfiguration=+&JobRequisitionShowDependents=+&JobReqTSAssessment=+&csk.IsoLocale=en&HROrganization=1&JobRequisitionApplicationProcessEntered=+&_=1650259979458")
                            jobObj['title'] = link['JobPostingListWebServices_ListOperationResponse'][
                                '__Description_translation___']
                            jobObj['url'] = self.baseUrl
                            isloaded, jres = self.get_request(url)
                            if isloaded:
                                jdata = jres.json()['Find_PostingDisplay_FormOperationResponse'][
                                    '__PositionDescription_translation___']
                                jobObj['description'] = str(jdata)
                                jobObj['location'] = link['JobPostingListWebServices_ListOperationResponse'][
                                    'LocationOfJob'].replace(":", ", ")
                                if jobObj['title'] != '' and jobObj['url'] != '':
                                    self.allJobs.append(jobObj)
                                    print(jobObj)
                        except (Exception, KeyError, AttributeError, ValueError) as e:
                            pass
            else:
                print("Job Not Found!")
        except Exception as e:
            print(e)
            self.iserror = True


if __name__ == "__main__":
    scraper = CRAWLER()
    scraper.process_logic()
    print(len(scraper.allJobs))
