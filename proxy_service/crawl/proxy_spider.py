from proxy_service.util.crawl_decorator import robust_crawl, robust_check
import re
import requests
import random
import time
from bs4 import BeautifulSoup, NavigableString


class ProxySpider(object):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    download_delay = 3

    @classmethod
    @robust_crawl
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

    @classmethod
    @robust_crawl
    def get_kuaidaili(cls):
        # http://www.kuaidaili.com/
        ipList = []
        m_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                     'Accept-Encoding': 'gzip, deflate, sdch',
                     'Accept-Language': 'zh-CN,zh;q=0.8',
                     'Connection': 'keep-alive',
                     'Host': 'www.kuaidaili.com',
                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        for i in range(1, 6):
            url = 'http://www.kuaidaili.com/proxylist/'+str(i)+'/'
            html = cls.requests_get(url, headers=m_headers)
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

    @classmethod
    @robust_crawl
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
        return ipList

    @classmethod
    @robust_crawl
    def get_66daili(cls):
        # http://www.66ip.cn/
        response = cls.requests_get('http://www.66ip.cn/nmtq.php?getnum=50&isp=0&anonymoustype=2&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip')
        if response==None:
            return None
        else:
            ipList = []
            ipstr_list = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:\d{1,5}', response.text)
            for ip in ipstr_list:
                ipList.append(ip)
            return ipList

    @classmethod
    @robust_crawl
    def get_xicidaili(cls):
        # http://www.xicidaili.com/
        response = cls.requests_get('http://www.xicidaili.com/nn/')
        if response == None:
            return None
        soup = BeautifulSoup(response.text, 'lxml')
        tr_list = soup.find('table', attrs={'id': 'ip_list'}).find_all('tr')
        ipList = []
        for tr_item in tr_list:
            td_list = tr_item.find_all('td')
            for td_item in td_list:
                td_str = td_item.get_text()
                td_str = ''.join(td_str.split())
                searchObj = re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}', td_str)
                if searchObj:
                    ip = searchObj.group()
                    port_str = td_item.find_next('td').get_text()
                    port_str = ''.join(port_str.split())
                    ipList.append(ip+':'+port_str)
        return ipList

    @classmethod
    @robust_crawl
    def get_mimiip(cls):
        # http://www.mimiip.com
        ipList = []
        for i in range(1, 3):
            response = cls.requests_get('http://www.mimiip.com/gngao/'+str(i))
            if response == None:
                continue
            soup = BeautifulSoup(response.text, 'lxml')
            tr_list = soup.find('table', attrs={'class': 'list'}).find_all('tr')
            for tr_item in tr_list:
                if tr_item.find('th'):
                    continue
                td_list = tr_item.find_all('td')
                for td_item in td_list:
                    td_str = td_item.get_text()
                    td_str = ''.join(td_str.split())
                    searchObj = re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}', td_str)
                    if searchObj:
                        ip = searchObj.group()
                        port_str = td_item.find_next('td').get_text()
                        port_str = ''.join(port_str.split())
                        ipList.append(ip + ':' + port_str)
        return ipList

    @classmethod
    @robust_crawl
    def get_ip181(cls):
        ipList = []
        for i in range(1, 4):
            response = cls.requests_get('http://www.ip181.com/daili/%d.html' % i)
            if response == None:
                continue
            soup = BeautifulSoup(response.text, 'lxml')
            tr_list = soup.find('div', attrs={'class': 'panel-body'}).find('table').find_all('tr')
            for tr_item in tr_list:
                td_list = tr_item.find_all('td')
                for td_item in td_list:
                    td_str = td_item.get_text()
                    td_str = ''.join(td_str.split())
                    searchObj = re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}', td_str)
                    if searchObj:
                        ip = searchObj.group()
                        port_str = td_item.find_next('td').get_text()
                        port_str = ''.join(port_str.split())
                        ipList.append(ip + ':' + port_str)
        return ipList

    @classmethod
    @robust_crawl
    def get_cybersyndrome(cls):
        ipList = []
        res = cls.requests_get('http://www.cybersyndrome.net/pla6.html')
        if(res == None):
            return ipList
        soup = BeautifulSoup(res.text, 'lxml')
        script_text = soup.find('div', id='content').find('ol').find_next('script').get_text()
         

    @classmethod
    def requests_get(cls, url, num_retries=3, proxy_str=None, headers=None):
        time.sleep(cls.download_delay)
        if headers == None:
            headers = {'User-Agent': random.choice(cls.user_agent_list)}
        timeout = 5
        if proxy_str == None:
            r = requests.get(url, headers=headers, timeout=timeout)
        else:
            proxy_dict = {'http': 'http://'+proxy_str}
            r = requests.get(url, headers=headers, timeout=timeout, proxies=proxy_dict)
        if r.status_code == 200:
            return r
        elif num_retries > 0:
            return cls.requests_get(url, num_retries=num_retries-1, proxy_str=proxy_str)
        else:
            print('Request error:', url)
            return None

    @classmethod
    @robust_crawl
    def get_host_ip(cls):
        default_host = '123.206.225.94'
        r = cls.requests_get('http://1212.ip138.com/ic.asp')
        if r == None:
            return default_host
        searchObj = re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}', r.text)
        if searchObj:
            return searchObj.group()
        else:
            return default_host

    @classmethod
    @robust_check
    def check_anonymous(cls, proxy_str):

        # host_ip = cls.get_host_ip()
        # response = cls.requests_get('http://www.cybersyndrome.net/env.cgi', proxy_str=proxy_str)
        # if response == None:
        #     return False
        # soup = BeautifulSoup(response.text, 'lxml')
        # try:
        #     proxy_tds = soup.find('td', string='REMOTE_ADDR').next_siblings
        # except:
        #     return False
        # has_find = False
        # check_proxy = ''
        # for td_item in proxy_tds:
        #     if isinstance(td_item, NavigableString):
        #         continue
        #     searchObj = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', td_item.get_text())
        #     if searchObj:
        #         has_find = True
        #         check_proxy = searchObj.group()
        #         check_proxy = ''.join(check_proxy.split())
        # if not has_find:
        #     return False
        # try:
        #     dd_list = soup.find('div', attrs={'id': 'sidebar'}).find('dl').find_all('dd')
        # except:
        #     return False
        # country = ''
        # anonymous = ''
        # for dd_item in dd_list:
        #     if dd_item.find('span') == None:
        #         country = dd_item.get_text()
        #         country = ''.join(country.split())
        #     else:
        #         anonymous = dd_item.find('span').get_text()
        #         anonymous = ''.join(anonymous.split())
        # print('check_proxy:', check_proxy, '; country:', country, '; anonymous:', anonymous)
        # if check_proxy == host_ip:
        #     return False
        # elif country != '中国(China)':
        #     return False
        # elif anonymous == 'Non-Anonymous':
        #     return False
        # else:
        #     return True

    @classmethod
    @robust_check
    def check_valid(cls, proxy_str):
        time.sleep(cls.download_delay)
        proxy_dict = {'http': 'http://'+proxy_str}
        headers = {'User-Agent': random.choice(cls.user_agent_list)}
        r = requests.get('http://www.baidu.com/', headers=headers, proxies=proxy_dict, timeout=5, verify=False)
        if r.status_code == 200:
            return True
        else:
            return False
