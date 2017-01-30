import requests
import re
import random
import requests
class ProxyMiddleware(object):
    def __init__(self):
        self.ipList = []
        html = requests.get('http://haoip.cc/tiqu.htm')
        ipListStr = re.findall(r'[.|:|0-9]+<br/>', html.text, re.S)
        ipAllList = []
        for list_str in ipListStr:
            ipAllList.append(list_str.replace(r'<br/>', ''))
        # 验证代理的有效性
        for ip in ipAllList:
            proxy = {'http': 'http://'+ip,
                     'https': 'https://'+ip}
            try:
                r = requests.get('http://www.baidu.com/', proxies=proxy, timeout=1, verify=False)
                if r.status_code == 200:
                    self.ipList.append('http://'+ip)
            except Exception as e:
                pass

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.ipList)
        # request.meta['proxy'] = 'http://110.206.127.136:9797'
        # print('My proxy:', request.meta['proxy'])

