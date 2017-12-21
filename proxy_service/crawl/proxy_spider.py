from proxy_service.util.crawl_decorator import robust_crawl, robust_check
import re
import requests
import random
import time
import urllib.parse
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
    def get_ip_pool(cls):
        ipList = []
        url = 'http://www.httpdaili.com/api.asp?ddbh=105357597956187379&noinfo=true&sl=5000'
        html = cls.requests_get(url)
        print(html)
        if html == None:
            return ipList
        urls = html.split('\r\n');
        for url in urls:
            if url and url != '':
                ipList.append(url)
        print(ipList)
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
    @robust_crawl
    def get_coderbusy(cls):
        urls = ['https://proxy.coderbusy.com/zh-cn/classical/country/cn.aspx']
        for i in range(2, 6):
            urls.append('https://proxy.coderbusy.com/zh-cn/classical/country/cn/p%d.aspx' % i)
        ipList = []
        for url in urls:
            res = cls.requests_get(url)
            if(res != None):
                soup = BeautifulSoup(res.text, 'lxml')
                lines = soup.find('table').find('tbody').find_all('tr')
                for line in lines:
                    hostSearch = re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}', line.find('td').get_text())
                    if hostSearch:
                        host = hostSearch.group()
                        port = line.find('td').find_next('td').get_text()
                        ipList.append(host + ':' + port)
        return ipList

    @classmethod
    @robust_crawl
    def get_cybersyndrome(cls):
        ipList = []
        res = requests.get('http://www.cybersyndrome.net/pla6.html')
        soup = BeautifulSoup(res.text, 'lxml')
        js_code = soup.find('ol').find_next('script').get_text()
        js_code = js_code.split(';')

        as_array = []
        searchObj_as = re.search(r'\[.*\]', js_code[0])
        if searchObj_as:
            as_array = eval(searchObj_as.group())

        ps = []
        searchObj_ps = re.search(r'\[.*\]', js_code[1])
        if searchObj_ps:
            ps = eval(searchObj_ps.group())

        cut_length = eval(js_code[2].replace('var n=', ''))
        as_array = as_array[cut_length:] + as_array[0:cut_length]

        proxies = [];
        for i, val in enumerate(as_array):
            if i % 4 == 0:
                single_proxy = str(val) + "."
            elif i % 4 == 3:
                single_proxy += str(val)
                single_proxy += ":" + str(ps[i / 4])
                proxies.append(single_proxy)
            else:
                single_proxy += (str(val) + ".")

        lines = soup.find('ol').find_all('li')
        for i, line in enumerate(lines):
            if line.a["id"] == "n%d" % (i + 1) and re.search(r'CN', line.a["onmouseover"]):
                ipList.append(proxies[i])
        return ipList
         

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
    def requests_post(cls, url, num_retries=3, proxy_str=None, headers=None):
        time.sleep(cls.download_delay)
        if headers == None:
            headers = {'User-Agent': random.choice(cls.user_agent_list)}
        timeout = 5
        if proxy_str == None:
            r = requests.post(url, headers=headers, timeout=timeout)
        else:
            proxy_dict = {'http': 'http://'+proxy_str}
            r = requests.post(url, headers=headers, timeout=timeout, proxies=proxy_dict)
        if r.status_code == 200:
            return r
        elif num_retries > 0:
            return cls.requests_post(url, num_retries=num_retries-1, proxy_str=proxy_str)
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
        m_headers = {
            "Host": "www.cybersyndrome.net",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "X-CS-Proxy": None,
            "X-CS-Sid": "start",
            "Origin": "http://www.cybersyndrome.net",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Referer": "http://www.cybersyndrome.net/pc.cgi",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
        };
        res = cls.requests_post('http://www.cybersyndrome.net/pc_s.cgi?t=' 
            + str(int(round(time.time()*1000))), headers=m_headers);
        if res == None or res.status_code != 200:
            return False
        sid = res.headers["X-CS-Sid"]

        m_headers["X-CS-Sid"] = sid
        m_headers["X-CS-Proxy"] = proxy_str
        res = cls.requests_post('http://www.cybersyndrome.net/pc_s.cgi?t=' 
            + str(int(round(time.time()*1000))), headers=m_headers);

        checkResult = urllib.parse.unquote(res.headers["X-CS-Message"])
        if checkResult.find('Anonymous') != -1 and checkResult.find('Non-Anonymous') == -1:
            return True
        else:
            return False

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
