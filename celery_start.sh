#!/bin/bash
redis-server --daemonize yes 
#celery -A celery_runner worker -l info 
celery multi start w1 w2 w3 w4 w5 -A celery_runner worker --loglevel=INFO --time-limit=6000 --concurrency=13

