from sf_record_spider.settings import PROXY_SERVICE_ADDRESS, PROXY_MAX_USE, DEFAULT_PROXY
import re
import requests
from scrapy import log


class ProxyMiddleware(object):

    def __init__(self):
        self.proxy = DEFAULT_PROXY
        self.proxy_use = 0
        self.max_use = int(PROXY_MAX_USE)
        self.proxy = self.update_proxy()

    def update_proxy(self):
        service_address = PROXY_SERVICE_ADDRESS+'get/'
        try:
            response = requests.get(service_address, timeout=5)
            if response.status_code == 200:
                searchObj = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', response.text)
                if searchObj:
                    return searchObj.group()
                else:
                    return self.proxy
            else:
                return self.proxy
        except:
            return self.proxy

    def process_request(self, request, spider):
        # if request.meta.get('change_proxy', False):
        #     self.proxy = self.update_proxy()
        #     msg = 'ProxyMiddleware: Change proxy to:' + self.proxy
        #     log.msg(msg, level=log.INFO)
        #     request.meta['change_proxy'] = False
        request.meta['proxy'] = 'http://'+self.proxy
        self.proxy_use += 1
        if self.proxy_use > self.max_use:
            self.proxy_use = 0
            self.proxy = self.update_proxy()
            msg = 'Change proxy to:'+self.proxy
            log.msg(msg, level=log.INFO)
        # request.meta['proxy'] = 'http://110.206.127.136:9797'

