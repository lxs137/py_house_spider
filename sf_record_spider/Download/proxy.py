from bs4 import BeautifulSoup
import re
import random
import requests
import time
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
            proxy = {'http': 'http://' + ip,
                     'https': 'https://' + ip}
            try:
                r = requests.get('http://www.baidu.com/', proxies=proxy, timeout=3, verify=False)
                if r.status_code == 200:
                    self.ipList.append('http://' + ip)
            except Exception as e:
                pass
        # headers = {'Host': 'www.kuaidaili.com',
        #            'Connection': 'keep-alive',
        #            'Upgrade-Insecure-Requests': '1',
        #            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #            'Accept-Encoding': 'gzip, deflate, sdch',
        #            'Accept-Language': 'zh-CN,zh;q=0.8',
        #            'Cookie': '_gat=1; channelid=0; sid=1486127313219185; _ga=GA1.2.290594692.1486128379; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1486128379; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1486128414'}
        # for i in range(1, 20):
        #     html = requests.get('http://www.kuaidaili.com/free/inha/'+str(i)+'/', headers=headers)
        #     soup = BeautifulSoup(html.text, 'html5lib')
        #     try:
        #         tr_list = soup.find('div', attrs={'id': 'list'}).find('tbody').find_all('tr')
        #     except:
        #         print('Html Error.')
        #         time.sleep(10)
        #     else:
        #         time.sleep(3)
        #         ipAllList = []
        #         for tr_item in tr_list:
        #             ip_str = tr_item.find('td', attrs={'data-title': 'IP'}).get_text()
        #             port_str = tr_item.find('td', attrs={'data-title': 'PORT'}).get_text()
        #             ipAllList.append(ip_str + ':' + port_str)
        #         for ip in ipAllList:
        #             proxy = {'http': 'http://' + ip,
        #                      'https': 'https://' + ip}
        #             try:
        #                 r = requests.get('http://www.baidu.com/', proxies=proxy, timeout=3)
        #                 if r.status_code == 200:
        #                     self.ipList.append('http://' + ip)
        #             except Exception as e:
        #                 print('Bad proxy.')

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.ipList)
        # request.meta['proxy'] = 'http://110.206.127.136:9797'
        # print('My proxy:', request.meta['proxy'])

