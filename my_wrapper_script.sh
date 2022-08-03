#!/bin/bash
  
# turn on bash's job control

  
# Start the primary process and put it in the background
./celery_start.sh &
  
# Start the helper process
./start.sh
  
# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns