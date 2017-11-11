FROM python:3

RUN apt-get update && apt-get install unzip

RUN cd /root \
	&& wget -O ssdb.zip --no-check-certificate https://github.com/ideawu/ssdb/archive/master.zip \
    && unzip ssdb.zip \
    && cd ssdb-master \
    && make \
    && make install

ENTRYPOINT ["/usr/local/ssdb/ssdb-server", "-d", "/usr/local/ssdb/ssdb.conf"]

EXPOSE 5000

EXPOSE 8888

CMD ["bash", "/root/proxy_service/start.sh"]