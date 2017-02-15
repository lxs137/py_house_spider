from sf_record_spider.settings import PROXY_SERVICE_ADDRESS, PROXY_MAX_USE, DEFAULT_PROXY
import re
import requests


class ProxyMiddleware(object):
    def __init__(self):
        self.proxy = DEFAULT_PROXY
        self.proxy_use = 0
        self.max_use = int(PROXY_MAX_USE)
        self.proxy = self.update_proxy(self.proxy)

    def update_proxy(self, old_proxy):
        service_address = PROXY_SERVICE_ADDRESS+'get/'
        try:
            response = requests.get(service_address, timeout=5)
            if response.status_code == 200:
                searchObj = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', response.text)
                if searchObj:
                    return searchObj.group()
                else:
                    return old_proxy
            else:
                return old_proxy
        except:
            return old_proxy

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://'+self.proxy
        self.proxy_use += 1
        if self.proxy_use > self.max_use:
            self.proxy_use = 0
            self.proxy = self.update_proxy(self.proxy)
        # request.meta['proxy'] = 'http://110.206.127.136:9797'

