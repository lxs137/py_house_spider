import requests
import re
import requests
from sf_house_spider.settings import DEFAULT_PROXY, PROXY_SERVICE_ADDRESS, PROXY_MAX_USE
class ProxyMiddleware(object):
    # def __init__(self):
    #     self.ipList = []
    #     html = requests.get('http://haoip.cc/tiqu.htm')
    #     ipListStr = re.findall(r'[.|:|0-9]+<br/>', html.text, re.S)
    #     ipAllList = []
    #     for list_str in ipListStr:
    #         ipAllList.append(list_str.replace(r'<br/>', ''))
    #     # 验证代理的有效性
    #     for ip in ipAllList:
    #         proxy = {'http': 'http://'+ip,
    #                  'https': 'https://'+ip}
    #         try:
    #             r = requests.get('http://www.baidu.com/', proxies=proxy, timeout=3, verify=False)
    #             if r.status_code == 200:
    #                 self.ipList.append('http://'+ip)
    #         except Exception as e:
    #             pass
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

