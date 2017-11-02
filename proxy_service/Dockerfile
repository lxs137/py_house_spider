FROM python:3

COPY . /root/proxy_service

RUN apt-get update && apt-get install unzip

RUN wget --no-check-certificate https://github.com/ideawu/ssdb/archive/master.zip \
    && unzip master \
    && cd ssdb-master \
    && make \
    && make install

RUN cd /root/proxy_service \
    && pip install -r requirements.txt

EXPOSE 5000

CMD ["bash", "/root/proxy_service/start.sh"]