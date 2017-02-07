from proxy_service.util.crawl_decorator import robust_crawl
import re
import requests
from bs4 import BeautifulSoup
class ProxySpider(object):

    @robust_crawl
    @classmethod
    def get_haoip(cls):
        html = requests.get('http://haoip.cc/tiqu.htm')
        ipListStr = re.findall(r'[.|:|0-9]+<br/>', html.text, re.S)
        ipList = []
        for list_str in ipListStr:
            ipList.append(list_str.replace(r'<br/>', ''))
        return ipList

    @robust_crawl
    @classmethod
    def get_kuaidaili(cls):
        pass


