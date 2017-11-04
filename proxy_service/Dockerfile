FROM python:3

RUN apt-get update && apt-get install unzip

RUN cd /root \
	&& wget -O ssdb.zip --no-check-certificate https://github.com/ideawu/ssdb/archive/master.zip \
    && unzip ssdb.zip \
    && cd ssdb-master \
    && make \
    && make install

RUN cd /root \
	&& wget -O spider.zip --no-check-certificate https://github.com/lxs137/py_house_spider/archive/master.zip \
	&& unzip spider.zip \
	&& cp -r py_house_spider-master/proxy_service /root

RUN cd /root/proxy_service \
    && pip install -r requirements.txt

EXPOSE 5000

CMD ["bash", "/root/proxy_service/start.sh"]