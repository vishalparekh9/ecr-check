import json
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from index import get_obj
import os
import time
import common as cf
#Token
token = 'GLASSDOOR_GLACIER'

class CRAWLER(object):
    def __init__(self):
        self.baseUrl = '' 
        self.location = 'glacier'
        self.getHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        }

        self.postHeader = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Accept':
            '*/*',
            'content-type': 'application/json',
            'apollographql-client-name': 'job-search',
            'apollographql-client-version': '0.16.17',
            'gd-csrf-token': ''
        }
        self.session = requests.session()
        self.domain = 'glassdoor.com'
        self.obj = deepcopy(get_obj())
        self.allJobs = []
        self.iserror = False
    def get_request(self, url):
        c = 0
        while True:
            try:
                res = self.session.get(url, headers=self.getHeaders) #,proxies={'http':'socks5://127.0.0.1:9050', 'https':'socks5://127.0.0.1:9050'})
                return True, res
            except Exception as e:
                print(e)
            print("Checking try again:" + str(c))
            time.sleep(0.5)
            c = c + 1
            if c > 3: break
        return False, False
    
    def post_request(self, dataDict):
        c = 0
        while True:
            try:
                posturl = 'https://www.glassdoor.com/graph'
                res = self.session.post(posturl, headers=self.postHeader, json = dataDict) #,proxies={'http':'socks5://127.0.0.1:9050', 'https':'socks5://127.0.0.1:9050'})
                return True, res
            except Exception as e:
                print(e)
            print("Checking try again:" + str(c))
            time.sleep(0.5)
            c = c + 1
            if c > 3: break
        return False, False
    
    def read_keywords(self):
        keywords = []
        try:
            with open(os.getcwd() + "/keywords") as f:
                lineList = f.readlines()
                for line in lineList:
                    keywords.append(line.strip().strip())
        except:
            pass
        return keywords
    
    def get_locations(self):
        try:
            url = 'https://www.glassdoor.com/findPopularLocationAjax.htm?maxLocationsToReturn=10&term='+str(self.location)+',%20us'
            isloaded, res = self.get_request(url)
            if len(res.json()) > 0:
                return res.json()
        except Exception as e:
            print(e)
            pass
        return False
    
    def html_decode(self,s):
        htmlCodes = (
                ("'", '&#39;'),
                ('"', '&quot;'),
                ('>', '&gt;'),
                ('<', '&lt;'),
                ('&', '&amp;')
            )
        for code in htmlCodes:
            s = s.replace(code[1], code[0])
        return s

    def get_details(self, links):
        self.allJobs = []
        for link in links:
            try:
                time.sleep(0.5)
                jobObj = deepcopy(self.obj)
                jobObj['domain'] = "glassdoor.com"
                jobObj['company'] = "Glassdoor"
                ao = link.split('ao=')[1].split('&')[0]
                jobListingId = link.split('jobListingId=')[1].split('&')[0]
                url = 'https://www.glassdoor.com/partner/jobListing.htm?ao='+str(ao)+'&vt=w&jobListingId='+str(jobListingId)
                jobObj['url'] = url
                isloaded, res = self.get_request(url)
                soup = BeautifulSoup(res.text, 'lxml')
                for script in soup.find_all('script',{'type':'application/ld+json'}):
                    jsn = json.loads(script.text)
                    if jsn['@type'] == 'JobPosting':
                        jobObj['title'] = jsn['title']
                        try:
                            jobObj['location'] = jsn['jobLocation']['address']['addressLocality'] 
                            jobObj['location'] += ', '+ jsn['jobLocation']['address']['addressRegion']
                            jobObj['location'] += ', '+ jsn['jobLocation']['address']['addressCountry']['name']
                        except:
                            pass
                        jobObj['description'] = self.html_decode(jsn['description'])
                        try:
                            jobObj['company'] = jsn['hiringOrganization']['name']
                            link = jsn['hiringOrganization']['sameAs'].lower().replace('http://','').replace('https://','').replace('www.','')
                            link = link.split('?')[0]
                            link = link.split('/')[0]
                            jobObj['domain'] = link
                        except:
                            pass
                        break
            except:
                pass
            if jobObj['domain'] == 'glassdoor.com':
                link = cf.domain_finder(jobObj['company'])
                if link: jobObj['domain'] = link
            if jobObj['title'] != '' and jobObj['url'] != '' and jobObj['location'] != '':
                self.allJobs.append(jobObj)
                print(jobObj['title'] + ' - ' + jobObj['location'] + ' - '+ jobObj['domain'])

    def get_page_details(self, loc, key):
        try:
            print("Loading main page")
            url = self.baseUrl
            isloaded, res = self.get_request(url)
            if not isloaded: return
            soup = BeautifulSoup(res.text, 'lxml')
            jsn = False
            jsn2 = False
            for script in soup.find_all('script'):
                if '"gdToken":' in script.text:
                    jsn = script.text.split('"gdToken":')[1].split(',')[0].replace('"','').replace('}','')
                if '"paginationCursors":' in script.text:
                    try:
                        jsn2 = script.text.split('"paginationCursors":')[1].split('}]')[0] + '}]'
                        jsn2 = json.loads(jsn2)
                    except:
                        pass
            if jsn == False and jsn2 == False: return
            gdToken = jsn
            self.postHeader['gd-csrf-token'] = gdToken
            pagination = jsn2
            links = soup.find_all('a',{'data-test':'job-link'})
            if len(links) > 0:
                output = [link.get('href') for link in links]
                self.get_details(output)
                cf.insert_rows(self.allJobs, self.site, self.iserror, self.domain, False)       

            page = 2
            isdata = True
            while isdata:
                print("Collecting page " + str(page))
                time.sleep(1)
                keyword = key
                locationId = str(loc['locationId'])
                locationType = 'CITY'
                if loc["locationType"] == 'S': locationType = 'STATE'
                pageNumber = str(page)
                pageCursor = ''
                if len(pagination) == 0: break
                for pag in pagination:
                    if str(pag['pageNumber']) == str(page):
                        pageCursor = str(pag['cursor'])
                        break
                postdata = {
                    "operationName": "JobSearchQuery",
                    "variables": {
                        "searchParams": {
                        "keyword": keyword,
                        "locationId": int(locationId),
                        "locationType": locationType,
                        "numPerPage": 30,
                        "searchType": "SR",
                        "pageNumber": int(pageNumber),
                        "pageCursor": pageCursor,
                        "filterParams": [
                            {
                            "filterKey": "includeNoSalaryJobs",
                            "values": "true"
                            },
                            {
                            "filterKey": "sortBy",
                            "values": "date_desc"
                            },
                            {
                            "filterKey": "fromAge",
                            "values": "3"
                            },
                            {
                            "filterKey": "sc.keyword",
                            "values": "software"
                            },
                            {
                            "filterKey": "locT",
                            "values": loc["locationType"]
                            },
                            {
                            "filterKey": "locId",
                            "values": str(loc['locationId'])
                            }
                        ],
                        "seoUrl": False
                        }
                    },
                    "query": "query JobSearchQuery($searchParams: SearchParams) {  jobListings(contextHolder: {searchParams: $searchParams}) {    ...SearchFragment    __typename  }}fragment SearchFragment on JobListingSearchResults {  adOrderJobLinkImpressionTracking  totalJobsCount  filterOptions  companiesLink  searchQueryGuid  indeedCtk  jobSearchTrackingKey  paginationCursors {    pageNumber    cursor    __typename  }  searchResultsMetadata {    cityPages {      cityBlurb      cityPagesStats {        bestCitiesForJobsRank        meanBaseSalary        population        unemploymentRate        __typename      }      displayName      employmentResources {        addressLine1        addressLine2        cityName        name        phoneNumber        state        zipCode        __typename      }      heroImage      isLandingExperience      locationId      numJobOpenings      popularSearches {        text        url        __typename      }      __typename    }    copyrightYear    footerVO {      countryMenu {        childNavigationLinks {          id          link          textKey          __typename        }        id        link        textKey        __typename      }      __typename    }    helpCenterDomain    helpCenterLocale    isPotentialBot    jobAlert {      jobAlertExists      promptedOnJobsSearch      promptingForJobClicks      __typename    }    jobSearchQuery    loggedIn    searchCriteria {      implicitLocation {        id        localizedDisplayName        type        __typename      }      keyword      location {        id        localizedDisplayName        shortName        localizedShortName        type        __typename      }      __typename    }    showMachineReadableJobs    showMissingSearchFieldTooltip    __typename  }  companyFilterOptions {    id    shortName    __typename  }  pageImpressionGuid  pageSlotId  relatedCompaniesLRP  relatedCompaniesZRP  relatedJobTitles  resourceLink  seoTableEnabled  jobListingSeoLinks {    linkItems {      position      url      __typename    }    __typename  }  jobListings {    jobview {      job {        descriptionFragments        eolHashCode        jobReqId        jobSource        jobTitleId        jobTitleText        listingId        __typename      }      jobListingAdminDetails {        adOrderId        cpcVal        importConfigId        jobListingId        jobSourceId        userEligibleForAdminJobDetails        __typename      }      overview {        id        name        shortName        squareLogoUrl        __typename      }      gaTrackerData {        trackingUrl        jobViewDisplayTimeMillis        requiresTracking        isIndeedJob        searchTypeCode        pageRequestGuid        isSponsoredFromJobListingHit        isSponsoredFromIndeed        __typename      }      header {        adOrderId        advertiserType        ageInDays        applyUrl        autoLoadApplyForm        easyApply        easyApplyMethod        employerNameFromSearch        jobLink        jobCountryId        jobResultTrackingKey        locId        locationName        locationType        needsCommission        normalizedJobTitle        organic        payPercentile90        payPercentile50        payPercentile10        hourlyWagePayPercentile {          payPercentile90          payPercentile50          payPercentile10          __typename        }        rating        salarySource        sponsored        payPeriod        payCurrency        savedJobId        sgocId        categoryMgocId        urgencySignal {          labelKey          messageKey          normalizedCount          __typename        }        __typename      }      __typename    }    __typename  }  __typename}"
                    }
                isloaded, res = self.post_request(postdata)
                if 'data' not in res.json(): break
                if 'jobListings' not in res.json()['data']: break
                if 'jobListings' not in res.json()['data']['jobListings']: break
                if len(res.json()['data']['jobListings']['jobListings']) == 0: break
                jobs = res.json()['data']['jobListings']['jobListings']
                output = [job['jobview']['header']['applyUrl'] for job in jobs]
                self.get_details(output)
                cf.insert_rows(self.allJobs, self.site, self.iserror, self.domain, False)
                if 'paginationCursors' not in res.json()['data']['jobListings']: break
                pagination = res.json()['data']['jobListings']['paginationCursors']
                page = page + 1
        except Exception as e:
            print(e)
    
    def process_logic(self):
        try:
            locations = self.get_locations()
            keywords = self.read_keywords()
            for loc in locations:
                for keyword in keywords:
                    time.sleep(0.5)
                    try:
                        time.sleep(0.5)
                        key = keyword.strip().lower()
                        #keyword
                        key = key.replace(' ','-')
                        locname = self.location.lower()
                        #locations
                        locname = locname.replace(' ','-')
                        print("Searching for keyword: " + str(keyword) + ' For location: ' + loc['label'])
                        self.baseUrl = 'https://www.glassdoor.com/Job/'+str(locname)+'-'+str(key)+'-SRCH_IL.0,'+str(len(locname))+'_I'+str(loc['id'])+'_KO'+str(len(locname) + 1)+','+str(len(locname) + 1 + len(key))+'_IP1.htm?fromAge=3&sortBy=date_desc'
                        self.get_page_details(loc, keyword.lower().strip())
                    except:
                        pass
                #     #remove
                #     break
                # #remove
                # break
        except Exception as e:
            print(e)
            self.iserror = True

if __name__ == "__main__":
    obj = CRAWLER()
    obj.process_logic()