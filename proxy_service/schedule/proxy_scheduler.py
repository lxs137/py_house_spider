from proxy_service.manager.proxy_manager import ProxyManager
from apscheduler.schedulers.blocking import BlockingScheduler
from proxy_service.util.crawl_decorator import my_log
import datetime
import threading


class ProxyScheduler(object):

    @my_log
    def __init__(self):
        self.manager = ProxyManager()
        self.scheduler = BlockingScheduler()
        self.lock = threading.Lock()
        refresh_run_time = datetime.datetime.now()+datetime.timedelta(minutes=1)
        clear_run_time = datetime.datetime.now()+datetime.timedelta(hours=36)
        # 每隔12个小时刷新一次代理池，每隔48小时清空可用代理并重新验证
        self.scheduler.add_job(self.refresh_proxy_pool, 'interval', hours=12, next_run_time=refresh_run_time)
        self.scheduler.add_job(self.clear_proxy_pool, 'interval', hours=48, next_run_time=clear_run_time)

    @my_log
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

    @my_log
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

    @my_log
    def start_scheduler(self):
        self.scheduler.start()

    @my_log
    def __del__(self):
        self.scheduler.remove_all_jobs()
        print('ProxyScheduler: remove all jobs.')

if __name__ == '__main__':
    m_scheduler = ProxyScheduler()
    m_scheduler.start_scheduler()