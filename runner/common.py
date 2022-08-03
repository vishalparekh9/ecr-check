from doctest import master
import mysql.connector
import re
import gc
from datetime import datetime
from dotenv import load_dotenv
import os


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
def update_status():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "update scraper_master set status='COMPLETE', finished_date=NOW() where id in (select scraper_id from job_scraper_monitor where scraper_id NOT IN (select scraper_id from job_scraper_monitor where status = 'PENDING' or status = 'INPROGRESS' group by scraper_id) group by scraper_id) and status !='COMPLETE' and is_infinite = 0"
        mycursor.execute(sql)
        mydb.commit()

        #Create a logs for the timeout scrapers
        sql = "INSERT INTO job_monitor_log (job_master_id, status, log_date, jobs_count, comment) SELECT job_mster_id as id, 'COMPLETE' as status, NOW(), found_jobs as  jobs_count, 'TIME OUT' as comment FROM job_scraper_monitor WHERE time_to_sec(TIMEDIFF(now(),started_at)) / 60 > 110 and status = 'INPROGRESS'"
        mycursor.execute(sql)
        mydb.commit()

        #update invalid crawlers
        sql = "update job_scraper_monitor set status='COMPLETE', updated_at=NOW(), comment='TIME OUT' WHERE time_to_sec(TIMEDIFF(now(),started_at)) / 60 > 110 and status = 'INPROGRESS'"
        mycursor.execute(sql)
        mydb.commit()
        return True
    except Exception as e:
        print(e)
    return False

def delete_old_crawler():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "delete from `scraper_cat_child` WHERE master_id in (select id from `scraper_master` where finished_date < now() - INTERVAL 6 day and is_test = 1)"
        mycursor.execute(sql)
        mydb.commit()

        sql = "delete from `job_board_list_cache` WHERE scraper_id in (select id from `scraper_master` where finished_date < now() - INTERVAL 6 day and is_test = 1)"
        mycursor.execute(sql)
        mydb.commit()

        sql = "delete from `job_scraper_monitor` WHERE scraper_id in (select id from `scraper_master` where finished_date < now() - INTERVAL 6 day and is_test = 1)"
        mycursor.execute(sql)
        mydb.commit()

        sql = "delete from `scraper_master` where finished_date < now() - INTERVAL 6 day and is_test = 1"
        mycursor.execute(sql)
        mydb.commit()

        return True
    except Exception as e:
        print(e)
        print("something went wrong on job crawler delete")
    return False

def auto_delete_live_sites_jobs_seven_days():
    try:
        output = []
        mydb = connector2()
        mycursor = mydb.cursor()
        sql = "DELETE FROM `add_jobs` WHERE updated_on < NOW() - INTERVAL 7 day"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
        print("seven days older jobs per crawler is finished")
        return True
    except Exception as e:
        print(e)
        print("something went wrong on job delete")
    return False

def auto_delete_jobs_seven_days():
    try:
        output = []
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT a.job_mster_id, a.updated_at FROM `job_scraper_monitor` a, `scraper_master` b WHERE a.status = 'COMPLETE' and a.scraper_id = b.id and b.is_test = 0 AND a.updated_at IS NOT NULL order by a.updated_at desc"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for (job_mster_id, updated_at) in result:
            obj ={
                'job_mster_id': job_mster_id,
                'updated_at': updated_at,
            }
            output.append(obj)
        for obj in output:
            try:
                sql = "DELETE FROM `job_board_list_not_matched` WHERE job_master_id = "+str(obj['job_mster_id'])+" and upd_ts < '"+str(obj['updated_at'])+"' - INTERVAL 7 day"
                mycursor.execute(sql)
                mydb.commit()
            except Exception as e:
                print(e)
                pass
            try:
                sql = "DELETE FROM `job_board_list` WHERE job_master_id = "+str(obj['job_mster_id'])+" and upd_ts < '"+str(obj['updated_at'])+"' - INTERVAL 7 day"
                mycursor.execute(sql)
                mydb.commit()
            except Exception as e:
                print(e)
                pass
        print("seven days older jobs per crawler is finished")
        mydb.close()
        return True
    except Exception as e:
        print(e)
        print("something went wrong on job delete")
    return False

def update_categories():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT a.id, a.cat_name, a.filed_name, a.cat_type from scraper_categories a"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for (id, cat_name, filed_name, cat_type) in result:
            obj ={
                'id': id,
                'cat_name': cat_name,
                'filed_name': filed_name,
                'cat_type': cat_type,
            }
            if obj['cat_type'] == 'db_field':
                sql = "update scraper_categories set sites_available = (SELECT count(id) as count FROM job_master_list_new where site_token != 'TOKEN' and "+str(obj['filed_name'])+" = 1) where id = " + str(obj['id'])
                mycursor.execute(sql)
                mydb.commit()
            else:
                sql = "update scraper_categories set sites_available = (SELECT count(id) as count FROM job_master_list_new where site_token != 'TOKEN' and career_url LIKE '%"+str(obj['filed_name'])+"%') where id = " + str(obj['id'])
                mycursor.execute(sql)
                mydb.commit()
        mydb.close()
    except Exception as e:
        print(e)
    return False

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

def find_and_add_tokens(data):
    masterid = 0
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        c = 1
        query = ""
        limit_count = 0
        for cat in data:
            masterid = cat['master_id']
            limit = ''
            if cat['is_test'] == 1 and cat['test_count'] != -1:
                limit_count = limit_count + cat['test_count']
                limit = ' limit '+ str(limit_count)
            try:
                if cat['cat_type'] == 'db_field':
                    sql = "update scraper_cat_child set total_urls = (SELECT count(id) as count FROM job_master_list_new where site_token != 'TOKEN' and "+str(cat['filed_name'])+" = 1) where id = " + str(cat['child_id'])
                    mycursor.execute(sql)
                    mydb.commit()
                    if c == 1:
                        query = " and (" + str(cat['filed_name'])+" = 1"
                    else:
                        query = query + " or " + str(cat['filed_name'])+" = 1"
                else:
                    sql = "update scraper_cat_child set total_urls = (SELECT count(id) as count FROM job_master_list_new where site_token != 'TOKEN' and career_url LIKE '%"+str(cat['filed_name'])+"%') where id = " + str(cat['child_id'])
                    mycursor.execute(sql)
                    mydb.commit()
                    if c == 1:
                        query = " and (" + "career_url LIKE '%"+str(cat['filed_name'])+"%'"
                    else:
                        query = query + " or " + "career_url LIKE '%"+str(cat['filed_name'])+"%'"
                c = c + 1
            except Exception as e:
                print(e)
                pass
        if c > 1: query = query + ")"
        if len(data) > 0:
            sql = "INSERT INTO job_scraper_monitor (job_mster_id, status, scraper_id, master_cat_id) SELECT id, 'PENDING', "+str(data[0]['master_id'])+" as status, "+str(data[0]['master_cat_id'])+" as master_cat_id FROM job_master_list_new where site_token != 'TOKEN'" + query + ' group by id ORDER BY RAND()'+str(limit)+';'
            mycursor.execute(sql)
            mydb.commit()
            if data[0]['is_active'] == 1:
                sql = "update scraper_master set comment = 'Setup Done', status = 'ACTIVE' where id = " +str(masterid)
            else:
                sql = "update scraper_master set comment = 'Setup Done', status = 'PAUSED' where id = " +str(masterid)
            mycursor.execute(sql)
            mydb.commit()
        mydb.close()
    except:
        sql = "update scraper_master set comment = 'Something wentwrong', status = 'FAILED' where id = " +str(masterid)
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()

def find_match_categories(id):
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT a.id, a.cat_id, a.master_id, b.cat_name, b.filed_name, b.cat_type, c.is_active, c.is_test, b.test_count, b.id as master_cat_id from scraper_cat_child a, scraper_categories b, scraper_master c where c.id = a.master_id and b.id = a.cat_id and a.master_id = " +str(id)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = []
        for (id, cat_id, master_id, cat_name, filed_name, cat_type, is_active, is_test, test_count, master_cat_id) in result:
            obj ={
                'child_id': id,
                'cat_id': cat_id,
                'cat_name': cat_name,
                'filed_name': filed_name,
                'master_id': master_id,
                'cat_type': cat_type,
                'is_active': is_active,
                'is_test': is_test,
                'test_count': test_count,
                'master_cat_id': master_cat_id
            }
            output.append(obj)
        mydb.close()
        find_and_add_tokens(output)
        return output
    except Exception as e:
        print(e)
    return False

def get_autopilot_master():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT scraper_name, id, is_infinite from scraper_master where is_infinite = 1"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = []
        for (scraper_name, id, is_infinite) in result:
            output.append({
                'id': id,
                'scraper_name': scraper_name,
                'is_infinite': is_infinite,
            })
        mydb.close()
        return output
    except Exception as e:
        print(e)
    return False

def check_for_all_infinite_finished():
    try:
        #first get all Auto pilot scrapers master id
        masters = get_autopilot_master()
        
        #check if the auto pilot sub scrapers are finished from the monitor
        mydb = connector()
        mycursor = mydb.cursor()
        deleteall = True
        for master in masters:
            sql = "SELECT count(*) as total FROM `job_scraper_monitor` WHERE status in ('PENDING','INPROGRESS') and scraper_id = " + str(master['id'])
            mycursor.execute(sql)
            result = mycursor.fetchall()
            output = [total[0] for total in result][0]
            if output > 0:
                deleteall = False
        
        #if finished then delete all the monitors and make master in init stage to reload again
        if deleteall:
            sql = "delete from job_scraper_monitor where scraper_id = " + str(master['id'])
            mycursor.execute(sql)
            mydb.commit()

            sql = "UPDATE `scraper_master` SET `status` = 'INITIATED' WHERE `scraper_master`.`id` =" + str(master['id'])
            mycursor.execute(sql)
            mydb.commit()
        else:
            print("Auto pilot is still running")
        mydb.close()
        return True
    except:
        pass
    return False

def add_remove_infinite_categories(master_id):
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        #Delete all old categories which is finished for the automation
        sql = "delete from scraper_cat_child where master_id = " + str(master_id)
        mycursor.execute(sql)
        mydb.commit()

        #Create new categories for the Auto pilot
        sql = 'insert into scraper_cat_child (master_id, cat_id) SELECT '+str(master_id)+' as master_id, id as cat_id FROM `scraper_categories` WHERE is_infinite = 1'
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
        return True
    except Exception as e:
        print(e)
        pass
    return False

def get_init_site():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT scraper_name, id, is_infinite from scraper_master where status = 'INITIATED' limit 5"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = []
        for (scraper_name, id, is_infinite) in result:
            output.append({
                'id': id,
                'scraper_name': scraper_name,
                'is_infinite': is_infinite,
            })
            sql = "update scraper_master set status='INITIALIZING...' where id = " + str(id)
            mycursor.execute(sql)
            mydb.commit()
        mydb.close()
        return output
    except Exception as e:
        print(e)
    return False

def get_keywords():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        sql = "SELECT keyword FROM keyword_master"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = [str(keyword[0]) for keyword in result]
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


def get_sites():
    try:
        mydb = connector()
        mycursor = mydb.cursor()
        #sql = "SELECT a.company_name as name, a.site_token as token, a.id as master_id, b.id, a.is_h1b_sponsor as is_h1b_sponsor FROM job_master_list as a, job_scraper_monitor as b WHERE b.status = 'PENDING' and b.job_mster_id = a.id limit 30"
        sql = "SELECT site_token from job_master_list_new where site_token != 'TOKEN'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        output = []
        output2 = []
        for (site_token) in result:
            output.append({
                'token': site_token[0],
                'result': False
            })
            output2.append(site_token[0])
        mydb.close()
        return output, output2
    except Exception as e:
        print(e)
    return False

def proxy():
    return {
        'http': 'http://user:pass@185.135.11.34:6007',
        'https': 'https://user:pass@185.135.11.34:6007',
    }