from doctest import master
import time
import mysql.connector
import re
import gc
from datetime import datetime
import requests
import functools
from requests.adapters import HTTPAdapter, Retry
from http import cookiejar
import threading
from copy import deepcopy
from dotenv import load_dotenv
import os
class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

def create_url(text):
    return re.sub('[^A-Za-z0-9]+', '-', text).lower()

def proxy():
    #Proxy should be in following format
    # return {
    #     'http': 'http://user:pass@185.135.11.34:6007',
    #     'https': 'https://user:pass@185.135.11.34:6007',
    # }
    # or
    return {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050',
    }
    # return {
    #     'http': 'http://testhc:testhc@dc.de-pr.oxylabs.io:40000',
    #     'https': 'http://testhc:testhc@dc.de-pr.oxylabs.io:40000'
    # }
    #return False

#Manage Session for whole app
def session_manager(obj):
    try:
        obj.session.request = functools.partial(obj.session.request, timeout=60)
        #Set Max retries for the session
        retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[ 500, 502, 503, 504 ])

        obj.session.mount('http://', HTTPAdapter(max_retries=retries))
        obj.session.mount('https://', HTTPAdapter(max_retries=retries))

        #disable cookie for specific domains
        domains = ['indeed.com','dice.com','zippia.com', 'careerbuilder.com', 'googlejobs.com', 'glassdoor.com']
        domainlen = len([domain for domain in domains if domain.lower() in obj.domain.lower().strip()])
        if domainlen > 0:
            obj.session.cookies.set_policy(BlockAll())
            if proxy(): obj.session.proxies = proxy()
    except:
        pass
    
def domain_finder(company):
    co = 0
    while True:
        company = ''.join(e for e in company if e.isalpha() or e.isspace() or e.isnumeric()).strip()
        try:
            time.sleep(0.2)
            session = requests.session()
            getHeaders = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            }
            url = 'https://autocomplete.clearbit.com/v1/companies/suggest?query=' +company
            res = session.get(url, headers=getHeaders, proxies=proxy(), timeout=5)
            if len(res.json()) == 0: break
            for jsn in res.json():
                if jsn['name'].lower().strip() == company.strip().lower():
                    return jsn['domain']
            break
        except:
            co = co + 1
            if co > 3:
                break
    return False

def doinsert(scraper):
    while True:
        time.sleep(5)
        try:
            if len(scraper.allJobs) > 50:
                insertjobs = deepcopy(scraper.allJobs)
                scraper.allJobs = []
                insert_rows(insertjobs, scraper.site, False, scraper.domain, False)
                insertjobs = []
                print("data Inserted by Thread")
        except:
            pass
        if scraper.cr_status == False:
            break
    
def execute(obj, site):
    try:
        print("Site Scraping: " + str(site['name']))
        session_manager(obj)
        print("Session Configured")
        obj.site = site
        domains = ['indeed.com', 'dice.com', 'zippia.com', 'careerbuilder.com', 'googlejobs.com', 'glassdoor.com']
        domainlen = len([domain for domain in domains if domain.lower() in obj.domain.lower().strip()])
        #threading code to insert data for every 20 records
        if domainlen == 0:
            obj.cr_status = True
            t = threading.Thread(target=doinsert, args=(obj,))
            t.start()
        obj.process_logic()
        obj.cr_status = False
        #threading code end
        print("Scraping Finished")
        insert_rows(obj.allJobs, site, obj.iserror, obj.domain)
    except Exception as e:
        print(e)
        print("* Error in running site "+obj.site)
    del(obj)
    del(site)
    gc.collect()

def connector():
    load_dotenv('.env') 
    host_env=os.getenv('host')
    user_env=os.getenv('user')
    passwd_env=os.getenv('passwd')
    database_env=os.getenv('database')
    auth_plugin_env=os.getenv('auth_plugin')
    return mysql.connector.connect(
            # host="65.108.144.228",
            # user="hccrawler",
            # passwd="Crawler#@(*)2022%",
            # database="job_scraper_test",
            # auth_plugin='mysql_native_password'
                host=host_env,
                user=user_env,
                passwd=passwd_env,
                database=database_env,
                auth_plugin=auth_plugin_env
            )

def connector2():
    return mysql.connector.connect(
            host="136.243.32.134",
            user="hicnslor_maindb",
            passwd="H6VW4z]Gnprb",
            database="hicnslor_maindb",
            auth_plugin='mysql_native_password'
            )
def connector3():
    return mysql.connector.connect(
            host="136.243.32.134",
            user="aditya_sendmaildb",
            passwd="sendmaildb@123",
            database="aditya_buildtab",
            auth_plugin='mysql_native_password'
            )
def started_crawler(id, message, status, isstarted):
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        q = ', updated_at=now() '
        if isstarted:
            q = ', created_at=now() '
        sql = "update job_scraper_monitor set status='"+str(status)+"', comment='"+str(message)+"'"+ q +"where id = " + str(id)
        mycursor.execute(sql)
        mydb.commit()
        if status == 'FAILED':
            sql = 'INSERT INTO job_monitor_log (job_master_id, status, log_date, jobs_count, comment) SELECT job_mster_id as id, status, NOW(), found_jobs as jobs_count, comment FROM job_scraper_monitor where id = '+str(id)
            mycursor.execute(sql)
            mydb.commit()
    except:
        pass

def get_devmode():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT is_active FROM scraper_setting where name = 'devmode' and is_active = 1"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = [is_active[0] for is_active in result][0]
        mydb.close()
        return True
    except Exception as e:
        print(e)
    return False

def get_limit():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT is_active FROM scraper_setting where name = 'scrapers'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = [is_active[0] for is_active in result][0]
        mydb.close()
        return output
    except Exception as e:
        print(e)
    return 30

def get_infinite_mode():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "select is_active from scraper_setting where name = 'infinte' and is_active = 1"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = [is_active[0] for is_active in result][0]
        mydb.close()
        return True
    except:
        pass
    return False

def get_keywords():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT keyword, category FROM keyword_master"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = [str(keyword) + '|' + str(category) for (keyword, category) in result]
        mydb.close()
        return output
    except Exception as e:
        print(e)
    return False

def get_locations():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT keyword FROM location_master"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = [str(keyword[0]) for keyword in result]
        mydb.close()
        return output
    except Exception as e:
        print(e)
    return False

def get_exclude_keywords():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT keyword FROM exclude_keywords"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = [str(keyword[0]) for keyword in result]
        mydb.close()
        return output
    except Exception as e:
        print(e)
    return False

def get_exclude_domains():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT domain FROM exclude_domains"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = [str(domain[0]) for domain in result]
        mydb.close()
        return output
    except Exception as e:
        print(e)
    return False

def get_pending_sites_test_env():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        limit = 10 #date 08-07-2022
        sql = "SELECT count(a.id) as count FROM job_scraper_monitor a, scraper_master b where a.scraper_id = b.id and b.is_test = 1 and a.status = 'INPROGRESS'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for (count) in result:
            limit = limit - count[0]
        
        #sql = "SELECT a.company_name as name, a.site_token as token, a.id as master_id, b.id, a.is_h1b_sponsor as is_h1b_sponsor FROM job_master_list as a, job_scraper_monitor as b WHERE b.status = 'PENDING' and b.job_mster_id = a.id limit 30"
        sql = "SELECT a.company_name as name, a.site_token as token, a.id as master_id, b.id, a.is_h1b_sponsor as is_h1b_sponsor, c.is_test, c.id as scraper_id, b.job_mster_id FROM job_master_list_new as a, job_scraper_monitor as b, scraper_master c WHERE c.id = b.scraper_id and c.status = 'ACTIVE' and b.status = 'PENDING' and b.job_mster_id = a.id and c.is_test = 1 order by RAND() limit " + str(limit)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = []
        for (name, token, master_id, id, is_h1b_sponsor, is_test, scraper_id, job_mster_id) in result:
            h1b= 'NO'
            if is_h1b_sponsor == 1:
                h1b = 'YES'
            output.append({
                'id': id,
                'master_id': master_id,
                'token': token,
                'name': name,
                'h1bvisa': h1b,
                'is_test': is_test,
                'scraper_id': scraper_id,
                'job_master_id': job_mster_id

            })
            sql = "update job_scraper_monitor set status='INPROGRESS', comment='Waiting for crawler', started_at=NOW() where id = " + str(id)
            mycursor.execute(sql)
            mydb.commit()

        mydb.close()
        return output
    except Exception as e:
        print(e)
    return False


def get_pending_sites_internal_env():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        limit = get_limit()
        sql = "SELECT count(a.id) as count FROM job_scraper_monitor a, scraper_master b where a.scraper_id = b.id and (b.is_test = 2 or b.is_test = 0) and a.status = 'INPROGRESS'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for (count) in result:
            limit = limit - count[0]
        if limit > 15:
            limit = 15 #08-06-2022 comment
        
        sql = "SELECT a.company_name as name, a.site_token as token, a.id as master_id, b.id, a.is_h1b_sponsor as is_h1b_sponsor, c.is_test, c.id as scraper_id, b.job_mster_id FROM job_master_list_new as a, job_scraper_monitor as b, scraper_master c WHERE c.id = b.scraper_id and c.status = 'ACTIVE' and b.status = 'PENDING' and b.job_mster_id = a.id and c.is_test = 2 order by RAND() limit " + str(limit)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = []
        for (name, token, master_id, id, is_h1b_sponsor, is_test, scraper_id, job_mster_id) in result:
            h1b= 'NO'
            if is_h1b_sponsor == 1:
                h1b = 'YES'
            output.append({
                'id': id,
                'master_id': master_id,
                'token': token,
                'name': name,
                'h1bvisa': h1b,
                'is_test': is_test,
                'scraper_id': scraper_id,
                'job_master_id': job_mster_id

            })
            sql = "update job_scraper_monitor set status='INPROGRESS', comment='Waiting for crawler', started_at=NOW() where id = " + str(id)
            mycursor.execute(sql)
            mydb.commit()

        mydb.close()
        return output
    except Exception as e:
        print(e)
    return []

def get_pending_sites_live():
    try:
        infinite = 0
        if get_infinite_mode():
            infinite = 1
        mydb = connector()
        mycursor = mydb.cursor()
        limit = get_limit() #80 changed on 15-06-2022
        sql = "SELECT count(a.id) as count FROM job_scraper_monitor a, scraper_master b where a.scraper_id = b.id and (b.is_test = 2 or b.is_test = 0) and a.status = 'INPROGRESS'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for (count) in result:
            limit = limit - count[0]
        if limit > 15:
            limit = 15 #08-06-2022 comment
        #sql = "SELECT a.company_name as name, a.site_token as token, a.id as master_id, b.id, a.is_h1b_sponsor as is_h1b_sponsor FROM job_master_list as a, job_scraper_monitor as b WHERE b.status = 'PENDING' and b.job_mster_id = a.id limit 30"
        sql = "SELECT a.company_name as name, a.site_token as token, a.id as master_id, b.id, a.is_h1b_sponsor as is_h1b_sponsor, c.is_test, c.id as scraper_id, b.job_mster_id FROM job_master_list_new as a, job_scraper_monitor as b, scraper_master c WHERE c.id = b.scraper_id and c.status = 'ACTIVE' and b.status = 'PENDING' and b.job_mster_id = a.id and c.is_infinite = "+str(infinite)+" and c.is_test = 0 order by RAND() limit " + str(limit)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = []
        for (name, token, master_id, id, is_h1b_sponsor, is_test, scraper_id, job_mster_id) in result:
            h1b= 'NO'
            if is_h1b_sponsor == 1:
                h1b = 'YES'
            output.append({
                'id': id,
                'master_id': master_id,
                'token': token,
                'name': name,
                'h1bvisa': h1b,
                'is_test': is_test,
                'scraper_id': scraper_id,
                'job_master_id': job_mster_id

            })
            sql = "update job_scraper_monitor set status='INPROGRESS', comment='Waiting for crawler', started_at=NOW() where id = " + str(id)
            mycursor.execute(sql)
            mydb.commit()

        mydb.close()
        return output
    except Exception as e:
        print(e)
    return False

def get_filtered_jobs(job_list):
    output = []
    notmatched = []
    try:
        keywords = get_keywords()
        locations = get_locations()
        exclude_keywords = get_exclude_keywords()
        exclude_domains = get_exclude_domains()
        domains = ['indeed.com', 'dice.com', 'glassdoor.com', 'careerbuilder.com','zippia.com', 'googlejobs.com']
        for job in job_list:
            try:
                job['is_match'] = 0
                job['matched_cat'] = ''
                job['matched_keyword'] = ''
                job['matched_location'] = ''
                job['matched_exclude'] = ''
                job['matched_domain'] = ''
                job['description'] = str(job['description']).encode('ascii', 'ignore').decode('ascii').replace("\n"," ").replace("\r"," ").replace("\t"," ")
                job['title'] = str(job['title']).encode('ascii', 'ignore').decode('ascii')
                job['location'] = str(job['location']).encode('ascii', 'ignore').decode('ascii')

                mylocation = ''.join(e for e in job['location'] if e.isalpha() or e.isspace() or e.isnumeric()).strip()
                mytitle = ''.join(e for e in job['title'] if e.isalpha() or e.isspace() or e.isnumeric()).strip()
                curdomain = job['domain'].lower().strip()

                #match exclude domain
                match = set([exclude for exclude in exclude_domains if exclude.lower() == curdomain.lower().strip()])
                excludedomain = sorted(match)
                excludedomainlen = len(excludedomain)

                #match exclude
                match = set([exclude for exclude in exclude_keywords if ' ' not in exclude.lower() if exclude.lower() in mytitle.lower().strip().split()])
                match2 = set([exclude for exclude in exclude_keywords if ' ' in exclude.lower() if exclude.lower() in mytitle.lower().strip()])
                excludematch = sorted(match)
                [excludematch.append(x) for x in sorted(match2) if x not in excludematch]
                excludelen = len(excludematch)
                
                #match keywords
                match = set([keyword for keyword in keywords if ' ' not in  keyword.lower().split('|')[0].lower() if keyword.lower().split('|')[0] in mytitle.lower().strip().split()])
                match2 = set([keyword for keyword in keywords if ' ' in  keyword.lower().split('|')[0].lower() if keyword.lower().split('|')[0] in mytitle.lower().strip()])
                finalmatch = sorted(match)
                [finalmatch.append(x) for x in sorted(match2) if x not in finalmatch]
                titlelen = len(finalmatch)

                #match location
                match = [location for location in locations if ' ' not in  location.lower() if location.lower() in mylocation.lower().strip().split()]
                match2 = [location for location in locations if ' ' in  location.lower() if location.lower() in mylocation.lower().strip()]
                locmatch = sorted(match)
                locmatch.extend(x for x in sorted(match2) if x not in locmatch)
                locationlen = len(locmatch)

                if locationlen == 0 and mylocation.lower().strip() == 'remote':
                    locationlen = 1
                    locmatch = ['remote']
                    
                domainlen = len([domain for domain in domains if domain.lower() in job['domain'].lower().strip()])

                #if titlelen > 0:
                cat = []
                uniquekey = []
                excludewords = []
                [cat.append(x.split('|')[1]) for x in finalmatch if x.split('|')[1] not in cat]
                [uniquekey.append(x.split('|')[0]) for x in finalmatch if x.split('|')[0] not in uniquekey]

                #code to check for the exclude does not available in matched keywords
                if excludelen > 0:
                    excludelen = 0
                    for key in excludematch:
                        if len(key) > 3:
                            if len([x for x in uniquekey if key.lower() in x.lower()]) == 0:
                                excludelen = 1
                                excludewords.append(key)
                        else:
                            excludelen = 1
                            excludewords.append(key)
                
                job['matched_cat'] = ' | '.join([x for x in sorted(cat)])
                job['matched_location'] = ' | '.join([x for x in locmatch])
                job['matched_keyword'] = ' | '.join([x.replace(" ","-") for x in uniquekey])
                job['matched_exclude'] = ' | '.join([x for x in excludewords])
                #job['matched_cat'] = ' | '.join([x.split('|')[1] for x in finalmatch])
                if domainlen > 0 or excludedomainlen > 0:
                    job['matched_domain'] = job['domain'].lower().strip()

                if titlelen > 0 and locationlen > 0 and domainlen == 0 and excludelen == 0 and excludedomainlen == 0:
                    job['is_match'] = 1
                    output.append(job)
                else:
                    job['is_match'] = 0
                    notmatched.append(job)
            except Exception as e:
                print("Matching error")
                job['is_match'] = 0
                job['matched_exclude'] = 'Matching error'
                notmatched.append(job)
    except Exception as e:
        print(e)
    return output, notmatched

def verify_output(newdata):
    try:
        if len(newdata) == 0: return False
        if 'myworkdayjobs.com' in newdata[0]['url'].lower(): return True
        r = requests.get(newdata[0]['url'].strip())
        print(r.headers["content-type"])
        if "text/html" in r.headers["content-type"] or "text/plain" in r.headers["content-type"]:    
            return True
        else:
            return False
    except:
        pass
    return True

def insert_rows(newdata, master, iserror, domain, is_crawler_finished=True):
    verified = True #verify_output(newdata) #date  08-07-2022
    print("hello verified")
    print(verified)
    data, notmatched = get_filtered_jobs(newdata)
    mydb = connector()
    mycursor = mydb.cursor()
    status = False
    jobrsponse = 'HTML'
    isdevmode = get_devmode()
    isinternal = False
    if master['is_test'] == 1:
        isdevmode = True
    elif master['is_test'] == 2:
        #if is_test is 2 means the data is scraped for internal use
        isinternal = True
    if not verified: jobrsponse = 'JSON'  

    #skip insert on execution when followin domains script execution is finished
    domains = ['indeed.com', 'glassdoor.com', 'careerbuilder.com', 'dice.com','zippia.com', 'googlejobs.com']
    domainlen = len([domain1 for domain1 in domains if domain1.lower() in domain.lower().strip()])
    isinsert = True
    if domainlen > 0 and is_crawler_finished:
        isinsert = False

    #insert internal data for the Team
    if len(newdata) > 0 and verified and isinsert and isdevmode == False and isinternal:
        print("Internal data")
        try:
            print("* Inserting new Data to database")
            #insert query with checking duplicate
            sql = "INSERT INTO job_board_list_internal (title, company, location, source, domains, apply_links, monitor_id, is_match, scraper_id, matched_cat, job_master_id, matched_location, matched_keyword, matched_exclude, matched_domain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql =  sql + "ON DUPLICATE KEY UPDATE location = VALUES(location);"
            val = []
            for item in newdata:
                sdomain = domain
                company = master['name']
                if item['domain'] != '':
                    sdomain = item['domain']
                if item['company'] != '':
                    company = item['company']
                sdomain = sdomain.replace('www.','').replace('WWW.','')
                val.append((item['title'], company, item['location'], company, sdomain, item['url'], str(master['id']), str(item['is_match']), str(master['scraper_id']), str(item['matched_cat']), str(master['master_id']), str(item['matched_location']), str(item['matched_keyword']), str(item['matched_exclude']), str(item['matched_domain'])))
            mycursor.executemany(sql, val)
            mydb.commit()

            print("* records inserted")
        except Exception as e:
            print(e)
            status = True

    if len(newdata) > 0 and verified and isinsert and isdevmode and isinternal == False:
        print("Dev data")
        try:
            print("* Inserting new Data to database")
            #insert query with checking duplicate
            sql = "INSERT INTO job_board_list_cache (title, company, location, source, domains, apply_links, monitor_id, is_match, scraper_id, matched_cat, job_master_id, matched_location, matched_keyword, matched_exclude, matched_domain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql =  sql + "ON DUPLICATE KEY UPDATE location = VALUES(location);"
            val = []
            for item in newdata:
                sdomain = domain
                company = master['name']
                if item['domain'] != '':
                    sdomain = item['domain']
                if item['company'] != '':
                    company = item['company']
                sdomain = sdomain.replace('www.','').replace('WWW.','')
                val.append((item['title'], company, item['location'], company, sdomain, item['url'], str(master['id']), str(item['is_match']), str(master['scraper_id']), str(item['matched_cat']), str(master['master_id']), str(item['matched_location']), str(item['matched_keyword']), str(item['matched_exclude']), str(item['matched_domain'])))
            mycursor.executemany(sql, val)
            mydb.commit()

            print("* records inserted")
        except Exception as e:
            print(e)
            status = True
    
    #Insert not matched data
    if len(notmatched) > 0 and isinsert and isdevmode == False and isinternal == False:
        #Insert not matched data
        print("Dev not matched data")
        try:            
            mydb_remote = connector()
            remotecursor = mydb_remote.cursor()
            print("* Inserting new Data to database")
            #insert query with checking duplicate
            sql = "INSERT INTO job_board_list_not_matched (title, company, location, ins_ts, domains, apply_links, h1b, job_category, job_master_id, upd_ts, matched_location, matched_keyword, matched_exclude, matched_domain) VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s)"
            sql =  sql + "ON DUPLICATE KEY UPDATE location = VALUES(location), upd_ts=NOW();"
            val = []
            for item in notmatched:
                sdomain = domain
                company = master['name']
                if item['domain'] != '':
                    sdomain = item['domain']
                if item['company'] != '':
                    company = item['company']
                sdomain = sdomain.replace('www.','').replace('WWW.','')
                val.append((item['title'], company, item['location'], sdomain, item['url'], master['h1bvisa'], str(item['matched_cat']), str(master['master_id']), str(item['matched_location']), str(item['matched_keyword']), str(item['matched_exclude']), str(item['matched_domain'])))
            remotecursor.executemany(sql, val)
            mydb_remote.commit()
            mydb_remote.close()
            print("* records inserted")
        except Exception as e:
            print(e)

    if len(data) > 0 and verified and isinsert and isdevmode == False and isinternal == False:
        # commented cache insert on 08-March-2022
        #Add Data to Automation tool table
        #Commented on 24-05-2022
        print("Live data")
        try:
            mydb_remote = connector() #connector3() #commented on 19-05-2022
            remotecursor = mydb_remote.cursor()
            print("* Inserting new Data to database")
            #insert query with checking duplicate
            sql = "INSERT INTO job_board_list (title, company, location, job_description, ins_ts, domains, apply_links, h1b, job_category, job_master_id, upd_ts, matched_location, matched_keyword, matched_exclude, matched_domain) VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s)"
            sql =  sql + "ON DUPLICATE KEY UPDATE job_description = VALUES(job_description), upd_ts=NOW();"
            val = []
            for item in data:
                sdomain = domain
                company = master['name']
                if item['domain'] != '':
                    sdomain = item['domain']
                if item['company'] != '':
                    company = item['company']
                sdomain = sdomain.replace('www.','').replace('WWW.','')
                val.append((item['title'], company, item['location'], item['description'], sdomain, item['url'], master['h1bvisa'], str(item['matched_cat']), str(master['master_id']), str(item['matched_location']), str(item['matched_keyword']), str(item['matched_exclude']), str(item['matched_domain'])))
            remotecursor.executemany(sql, val)
            mydb_remote.commit()
            mydb_remote.close()
            print("* records inserted")
        except Exception as e:
            print(e)
            status = True
        
        #add data to jobs list
        try:
            mydb_remote = connector2()
            remotecursor = mydb_remote.cursor()
            print("* Inserting new Data to database")
            #insert query with checking duplicate
            sql = "INSERT INTO add_jobs (title, company, location, job_description, date, logo, link, job_expired, created_on, posted_by, h1b, search_keywords, updated_on) VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s, NOW(), %s, %s, %s, NOW())"
            sql =  sql + "ON DUPLICATE KEY UPDATE job_description = VALUES(job_description), search_keywords = VALUES(search_keywords), updated_on = NOW();"
            val = []
            for item in data:
                sdomain = domain
                company = master['name']
                if item['domain'] != '':
                    sdomain = item['domain']
                if item['company'] != '':
                    company = item['company']
                item['matched_keyword'] = item['matched_keyword'].lower() + ', ' + item['location'].lower() + ', ' + company.lower()
                item['matched_keyword'] = item['matched_keyword'].replace(", ","^").replace(",","^")
                item['matched_keyword'] = item['matched_keyword'].replace(" ","-")
                item['matched_keyword'] = item['matched_keyword'].replace("^",", ")
                sdomain = sdomain.replace('www.','').replace('WWW.','')
                if '<h' in item['description'] or '<div' in item['description'] or '<span' in item['description'] or '<table' in item['description'] or '<li' in item['description'] or '<p' in item['description']:
                    val.append((item['title'], company, item['location'], item['description'], sdomain, item['url'], '', 'Web Scraper', master['h1bvisa'], item['matched_keyword']))
            if len(val) > 0:
                remotecursor.executemany(sql, val)
                mydb_remote.commit()
            mydb_remote.close()
            print("* records inserted")
        except Exception as e:
            print(e)
            status = True
    #Changing status to finish or Failed based on status of crawler
    sql = "update job_scraper_monitor set response_type='"+str(jobrsponse)+"', updated_at=now(), status='COMPLETE', found_jobs = found_jobs + "+str(len(newdata))+", matched_jobs= matched_jobs + "+str(len(data))+", comment='SUCCESS' where id = " + str(master['id'])
    status_text = 'COMPLETE'
    comment_text='SUCCESS'
    if status or iserror:
        status_text = 'FAILED'
        comment_text='Something went wrong'
        if status:
            sql = "update job_scraper_monitor set response_type='"+str(jobrsponse)+"', updated_at=now(), status='FAILED', found_jobs= found_jobs + "+str(len(newdata))+", matched_jobs= matched_jobs + "+str(len(data))+", comment='QUERY Failed' where id = " + str(master['id'])
        else:
            sql = "update job_scraper_monitor set response_type='"+str(jobrsponse)+"', updated_at=now(), status='FAILED', found_jobs='0', matched_jobs='0', comment='Scraper Failed' where id = " + str(master['id'])
            
    #If crawler execusion is finished then update status
    if is_crawler_finished == False:
        sql = "UPDATE `job_scraper_monitor` set found_jobs = found_jobs + "+str(len(newdata))+", matched_jobs = matched_jobs + "+str(len(data))+" WHERE id = " + str(master['id'])
    if isinsert == False:
        sql = "UPDATE `job_scraper_monitor` set response_type='"+str(jobrsponse)+"', updated_at=now(), comment='"+str(comment_text)+"', status='"+str(status_text)+"' WHERE id = " + str(master['id'])
    mycursor.execute(sql)
    mydb.commit()

    if 'status=' in sql:
        sql = 'INSERT INTO job_monitor_log (job_master_id, status, log_date, jobs_count, comment) SELECT job_mster_id as id, status, NOW(), found_jobs as jobs_count, comment FROM job_scraper_monitor where id = '+str(master['id'])
        mycursor.execute(sql)
        mydb.commit()
    mydb.close()
    return status