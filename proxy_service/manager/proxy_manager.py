from proxy_service.database.SSDB import SSDBManager
from proxy_service.crawl.proxy_spider import ProxySpider


class ProxyManager(object):
    valid_list = 'valid_proxy_list'
    all_list = 'unchecked_proxy_list'

    def __init__(self):
        self.db_conn = SSDBManager()

    def get_proxy(self):
        proxy = self.db_conn.get_list_front(ProxyManager.valid_list)
        return proxy

    def get_all_proxies(self):
        proxy_list = self.db_conn.get_list(ProxyManager.valid_list)
        if proxy_list == None:
            return []
        else:
            return proxy_list

    def insert_unchecked_proxy(self, proxy_list):
        all_list = self.db_conn.get_list(ProxyManager.all_list)
        if all_list == None or len(all_list) == 0:
            all_list = proxy_list
        else:
            for proxy in proxy_list:
                if all_list.count(proxy) == 0:
                    all_list.append(proxy)
        self.db_conn.create_list(ProxyManager.all_list, all_list)

    def get_unchecked_proxy(self):
        unchecked_list = []
        extend_list = []
        extend_list.append(ProxySpider.get_haoip())
        extend_list.append(ProxySpider.get_kuaidaili())
        extend_list.append(ProxySpider.get_66daili())
        extend_list.append(ProxySpider.get_youdaili())
        extend_list.append(ProxySpider.get_xicidaili())
        for list_item in extend_list:
            if list_item != None:
                unchecked_list.extend(list_item)
        return unchecked_list

    def check_proxies(self):
        all_list = self.db_conn.get_list(ProxyManager.all_list)
        valid_proxy = []
        if all_list == None or len(all_list) == 0:
            return
        for proxy in all_list:
            if ProxySpider.check_valid(proxy) and ProxySpider.check_anonymous(proxy):
                valid_proxy.append(proxy)
        self.db_conn.create_list(ProxyManager.valid_list, valid_proxy)

    def clear_list(self, name):
        self.db_conn.clear_list(name)