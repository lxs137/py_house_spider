from proxy_service.database.SSDB import SSDBManager
from proxy_service.crawl.proxy_spider import ProxySpider
from proxy_service.util.crawl_decorator import my_log
from twisted.internet import reactor
import functools
import threading
import time


class ProxyManager(object):
    valid_list = 'valid_proxy_list'
    all_list = 'unchecked_proxy_list'

    def __init__(self):
        self.db_conn = SSDBManager()
        self.valid_proxy = []
        self.unchecked_proxy = 0
        self.mutli_thread_lock = None
        self.stop_reactor_lock = None

    def get_proxy(self):
        proxy = self.db_conn.get_list_front(ProxyManager.valid_list)
        return proxy

    def get_all_proxies(self):
        proxy_list = self.db_conn.get_list(ProxyManager.valid_list)
        if proxy_list == None:
            return []
        else:
            return proxy_list

    def get_unchecked_proxies(self):
        proxy_list = self.db_conn.get_list(ProxyManager.all_list)
        if proxy_list == None:
            return []
        else:
            return proxy_list

    def insert_proxy_list(self, name, proxy_list):
        all_list = self.db_conn.get_list(name)
        if all_list == None or len(all_list) == 0:
            all_list = proxy_list or []
        else:
            for proxy in proxy_list:
                if all_list.count(proxy) == 0:
                    all_list.append(proxy)
        self.db_conn.create_list(name, all_list)

    def get_unchecked_proxy(self):
        unchecked_list = []
        extend_list = []

        extend_list.append(ProxySpider.get_ip_pool())
        print('IP pool done: ', extend_list[len(extend_list) - 1])

        # extend_list.append(ProxySpider.get_kuaidaili())
        # print('kuaidaili done:', extend_list[len(extend_list) - 1])

        # extend_list.append(ProxySpider.get_66daili())
        # print('66daili done:', extend_list[len(extend_list) - 1])

        # extend_list.append(ProxySpider.get_xicidaili())
        # print('xicidaili done:', extend_list[len(extend_list) - 1])

        # extend_list.append(ProxySpider.get_mimiip())
        # print('mimidaili done:', extend_list[len(extend_list) - 1])

        # extend_list.append(ProxySpider.get_ip181())
        # print('ip181daili done:', extend_list[len(extend_list) - 1])

        # extend_list.append(ProxySpider.get_coderbusy())
        # print('codebusy done:', extend_list[len(extend_list) - 1])
        
        for list_item in extend_list:
            if list_item != None:
                unchecked_list.extend(list_item)
        return unchecked_list

    def check_proxies(self):
        all_list = self.db_conn.get_list(ProxyManager.all_list)
        if all_list == None or len(all_list) == 0:
            return []
        self.valid_proxy = []
        self.unchecked_proxy = 0
        self.mutli_thread_lock = threading.Lock()
        self.stop_reactor_lock = threading.Lock()
        mutli_check_func = functools.partial(self.mutli_thread_check, all_list)
        if reactor._startedBefore:
            reactor.__init__()
        # callFromThread将阻塞调用该函数的线程
        # 将启动多线程的函数放入reactor的主线程，便于停止
        reactor.callFromThread(mutli_check_func)
        reactor.run()
        return self.valid_proxy

    def mutli_thread_check(self, all_list):
        self.stop_reactor_lock.acquire()
        for proxy in all_list:
            self.unchecked_proxy += 1
            check_func = functools.partial(self.check_proxy, proxy)
            # callInThread不阻塞调用该函数的线程，而是将函数放入reactor的线程池中运行
            # 将代理验证操作放入twisted线程池中执行
            reactor.callInThread(check_func)
        self.stop_reactor_lock.acquire()
        reactor.stop()
        self.stop_reactor_lock.release()

    @my_log(log_name='schedule.log')
    def check_proxy(self, proxy):
        check_result = ProxySpider.check_valid(proxy) and ProxySpider.check_anonymous(proxy)
        self.mutli_thread_lock.acquire()
        self.unchecked_proxy -= 1
        if check_result:
            print(proxy, ': valid')
            self.valid_proxy.append(proxy)
        else:
            print(proxy, ': not valid')
        # 当所有代理验证完毕后，释放阻塞mutli_thread_check函数的锁，退出reactor
        if self.unchecked_proxy <= 0:
            self.stop_reactor_lock.release()
        self.mutli_thread_lock.release()

    def clear_list(self, name):
        self.db_conn.clear_list(name)
