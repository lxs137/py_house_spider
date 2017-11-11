#!/bin/bash

export PYTHONPATH=/root

# download source code
cd /root
wget -O spider.zip --no-check-certificate https://github.com/lxs137/py_house_spider/archive/master.zip
unzip spider.zip
cp -r py_house_spider-master/proxy_service /root

cd /root/proxy_service
pip install -r requirements.txt

# start ssdb
cd /usr/local/ssdb 
./ssdb-server -d ssdb.conf

# start Flask server
cd /root/proxy_service/web_service
gunicorn -D -w 2 -b 0.0.0.0:5000 flask_service:app

python /root/proxy_service/schedule/proxy_scheduler.py