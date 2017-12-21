from proxy_service.manager.proxy_manager import ProxyManager
from apscheduler.schedulers.blocking import BlockingScheduler
from proxy_service.util.crawl_decorator import my_log
import datetime
import threading
import os
import sys


class ProxyScheduler(object):

    # @my_log(log_name='schedule.log')
    def __init__(self, refresh_freq):
        self.manager = ProxyManager()
        self.scheduler = BlockingScheduler()
        self.lock = threading.Lock()
        refresh_run_time = datetime.datetime.now()+datetime.timedelta(minutes=1)
        clear_run_time = datetime.datetime.now()+datetime.timedelta(hours=12)
        # 每隔6个小时刷新一次代理池，每隔24小时清空可用代理并重新验证
        self.scheduler.add_job(self.refresh_proxy_pool, 'interval', hours=refresh_freq, next_run_time=refresh_run_time)
        self.scheduler.add_job(self.clear_proxy_pool, 'interval', hours=24, next_run_time=clear_run_time)

    # @my_log(log_name='schedule.log')
    def refresh_proxy_pool(self):
        self.lock.acquire()
        print('Refresh proxy pool: start.')
        print(datetime.datetime.now())
        unchecked_list = self.manager.get_unchecked_proxy()
        self.manager.insert_proxy_list(ProxyManager.all_list, unchecked_list)
        valid_list = self.manager.check_proxies()
        self.manager.insert_proxy_list(ProxyManager.valid_list, valid_list)
        print('Refresh proxy pool: done.')
        self.lock.release()

    # @my_log(log_name='schedule.log')
    def clear_proxy_pool(self):
        self.lock.acquire()
        print('Clear proxy pool: start.')
        print(datetime.datetime.now())
        self.manager.clear_list(ProxyManager.all_list)
        overdue_list = self.manager.get_all_proxies()
        self.manager.insert_proxy_list(ProxyManager.all_list, overdue_list)
        self.manager.clear_list(ProxyManager.valid_list)
        print('Clear proxy pool: done.')
        self.lock.release()

    # @my_log(log_name='schedule.log')
    def start_scheduler(self):
        self.scheduler.start()

    # @my_log(log_name='schedule.log')
    def __del__(self):
        self.scheduler.remove_all_jobs()
        print('ProxyScheduler: remove all jobs.')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        m_scheduler = ProxyScheduler(int(sys.argv[1]))
    else:
        m_scheduler = ProxyScheduler(3)
    m_scheduler.start_scheduler()