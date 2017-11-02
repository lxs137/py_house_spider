#!/bin/bash

export PYTHONPATH=/root

# start ssdb
cd /usr/local/ssdb 
./ssdb-server -d ssdb.conf

# start Flask server
cd /root/proxy_service/web_service
gunicorn -D -w 2 -b 0.0.0.0:5000 flask_service:app

python /root/proxy_service/schedule/proxy_scheduler.py