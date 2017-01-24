import requests
import re
import random
class ProxyMiddleware(object):
    def __init__(self):
        self.ipList = []
        html = requests.get('http://haoip.cc/tiqu.htm')
        ipListStr = re.findall(r'[.|:|0-9]+<br/>', html.text, re.S)
        for list_str in ipListStr:
            self.ipList.append('http://'+list_str.replace(r'<br/>', ''))

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.ipList)
        # request.meta['proxy'] = 'http://202.106.16.36:3128'
        # print('My proxy:', request.meta['proxy'])

