from celery import Celery
import sitedirectory as scraper
#custom files imports
import common as cf

#app = Celery('handler2', broker='amqp://aoierdli:m0hd42A1zS-Xkymw0a5GeyGdYhkDfz_y@woodpecker.rmq.cloudamqp.com/aoierdli', result_backend ='db+mysql://crawler1:Celery123%hh@localhost/celery')
app = Celery('handler2', broker='redis://127.0.0.1:6379/0', result_backend =  'redis://localhost:6379/0') #'db+mysql://crawler1:Celery123%hh@localhost/celery')

@app.task
def thread(site):
    try:
        print(site)
        obj = scraper.SITEDIRECTORY(site).get_object()
        if obj:
            cf.started_crawler(site['id'], 'CRAWLER Started', 'INPROGRESS', True)
            cf.execute(obj, site)
        else:
            cf.started_crawler(site['id'], 'CRAWLER NOT Found', 'FAILED', False)
    except:
        cf.started_crawler(site['id'], 'Time Out error (1.5 hours)', 'FAILED', False)
        
            
            
            
