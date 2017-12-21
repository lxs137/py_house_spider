FROM registry.njuics.cn/fluentd/python:3.5

RUN apt-get update && apt-get install unzip

RUN cd /root \
	&& wget -O ssdb.zip --no-check-certificate https://github.com/ideawu/ssdb/archive/master.zip \
    && unzip ssdb.zip \
    && cd ssdb-master \
    && make \
    && make install

RUN cd /root \
	&& wget -O start.sh https://raw.githubusercontent.com/lxs137/py_house_spider/master/proxy_service/start.sh

RUN cd /root \
	&& wget -O requirements.txt https://raw.githubusercontent.com/lxs137/py_house_spider/master/proxy_service/requirements.txt \
	&& pip install -r requirements.txt

EXPOSE 5000

EXPOSE 8888

CMD ["bash", "/root/start.sh"]