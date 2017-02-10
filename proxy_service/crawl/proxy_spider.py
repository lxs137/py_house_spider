from proxy_service.util.crawl_decorator import robust_crawl
import re
import requests
import random
import time
from bs4 import BeautifulSoup
class ProxySpider(object):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    download_delay = 2

    @robust_crawl
    @classmethod
    def get_haoip(cls):
        # http://haoip.cc/
        html = cls.requests_get('http://haoip.cc/tiqu.htm')
        if html == None:
            return None
        ipListStr = re.findall(r'[.|:|0-9]+<br/>', html.text, re.S)
        ipList = []
        for list_str in ipListStr:
            ipList.append(list_str.replace(r'<br/>', ''))
        return ipList

    @robust_crawl
    @classmethod
    def get_kuaidaili(cls):
        # http://www.kuaidaili.com/
        ipList = []
        for i in range(1, 11):
            url = 'http://www.kuaidaili.com/proxylist/'+str(i)+'/'
            html = cls.requests_get(url)
            if html == None:
                continue
            soup = BeautifulSoup(html.text, 'lxml')
            tr_list = soup.find('div', attrs={'id': 'index_free_list'}).find('tbody').find_all('tr')
            for tr_item in tr_list:
                if tr_item.find('td', attrs={'data-title': '匿名度'}).get_text() == '透明':
                    continue
                else:
                    ip = tr_item.find('td', attrs={'data-title': 'IP'}).get_text()
                    port = tr_item.find('td', attrs={'data-title': 'PORT'}).get_text()
                    ipList.append(ip+':'+port)
        return ipList

    @robust_crawl
    @classmethod
    def get_youdaili(cls):
        # http://www.youdaili.net/
        ipList = []
        base_html = cls.requests_get('http://www.youdaili.net/Daili/http')
        if base_html == None:
            return None
        soup = BeautifulSoup(base_html.text, 'lxml')
        detail_url = soup.find('div', attrs={'class': 'chunlist'}).find_all('li')[0]\
            .find('p').find('a')['href']
        detail_html = cls.requests_get(detail_url)
        if detail_html == None:
            return None
        soup = BeautifulSoup(detail_html.text, 'lxml')
        page_str = soup.find('div', attrs={'class': 'pagebreak'}).find_all('li')[0]\
            .find('a').get_text()
        max_page = int(re.search('[0-9]+', page_str).group())
        for i in range(1, max_page+1):
            if i > 1:
                page_html = cls.requests_get(detail_url[:detail_url.find('.html')]\
                                             +'_'+str(i)+'.html')
                if page_html == None:
                    return None
                soup = BeautifulSoup(page_html.text, 'lxml')
            p_list = soup.find('div', attrs={'class': 'arc'})\
                .find('div', attrs={'class': 'content'}).find_all('p')
            for p_item in p_list:
                ip_str = p_item.get_text()
                matchObj = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', ip_str)
                if matchObj:
                    ipList.append(matchObj.group())
        pass

    @classmethod
    def requests_get(cls, url, num_retries=3):
        time.sleep(cls.download_delay)
        headers = {'User-Agent': random.choice(cls.user_agent_list)}
        timeout = 3
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code == 200:
            return r
        elif num_retries > 0:
            return cls.requests_get(url, num_retries=num_retries-1)
        else:
            print('Request error:', url)
            return None




