from proxy_service.manager.proxy_manager import ProxyManager
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
class ProxyScheduler(object):
    def __init__(self):
        self.manager = ProxyManager()
        self.scheduler = BlockingScheduler()
        refresh_run_time = datetime.datetime.now()+datetime.timedelta(minutes=1)
        clear_run_time = datetime.datetime.now()+datetime.timedelta(hours=36)
        # 每隔12个小时刷新一次代理池，每隔48小时清空可用代理并重新验证
        self.scheduler.add_job(self.refresh_proxy_pool, 'interval', hours=12, next_run_time=refresh_run_time)
        self.scheduler.add_job(self.clear_proxy_pool, 'interval', hours=48, next_run_time=clear_run_time)

    def refresh_proxy_pool(self):
        print('Refresh proxy pool: start.')
        print(datetime.datetime.now())
        unchecked_list = self.manager.get_unchecked_proxy()
        self.manager.insert_unchecked_proxy(unchecked_list)
        self.manager.check_proxies()
        print('Refresh proxy pool: done.')

    def clear_proxy_pool(self):
        print('Clear proxy pool: start.')
        print(datetime.datetime.now())
        self.manager.clear_list(ProxyManager.all_list)
        overdue_list = self.manager.get_all_proxies()
        self.manager.insert_unchecked_proxy(overdue_list)
        self.manager.clear_list(ProxyManager.valid_list)
        print('Clear proxy pool: done.')

    def start_scheduler(self):
        self.scheduler.start()

    def __del__(self):
        self.scheduler.remove_all_jobs()
        print('ProxyScheduler: remove all jobs.')

if __name__ == '__main__':
    m_scheduler = ProxyScheduler()
    m_scheduler.start_scheduler()