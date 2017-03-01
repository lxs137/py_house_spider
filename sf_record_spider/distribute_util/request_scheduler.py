from sf_house_spider.distribute_util.request_dupefilter import RedisDupeFilter
from redis import Redis
from sf_house_spider.distribute_util.request_queue import RedisRequestQueue


class RedisScheduler(object):
    def __init__(self, redis_server, persisit, stats, settings):
        self.server = redis_server
        self.spider = None
        self.queue = None
        self.dupefilter = None
        self.persist = persisit
        self.stats = stats
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        server = Redis(host=settings.get('REDIS_HOST', 'localhost'),
                       port=settings.get('REDIS_PORT', 6379),
                       password=settings.get('REDIS_PASSWORD', None))
        persist = settings.get('SCHEDULER_PERSIST', False)
        return cls(redis_server=server, persisit=persist,
                   stats=crawler.stats, settings=settings)

    def open(self, spider):
        dupefilter_key = self.settings.get('REDIS_DUPEFILTER_KEY',
                                           'DUPEFILTER_' + spider.name)
        queue_key = self.settings.get('REDIS_QUEUE_KEY',
                                      'QUEUE_' + spider.name)
        self.spider = spider
        self.dupefilter = RedisDupeFilter(self.server, dupefilter_key)
        self.queue = RedisRequestQueue(self.server, spider, queue_key)
        if len(self.queue) > 0:
            msg = 'Resuming ' + str(len(self.queue)) + ' requests from ' + queue_key
            spider.log(msg)

    def close(self, reason):
        if not self.persist:
            self.queue.close(reason)
            self.dupefilter.close(reason)

    def next_request(self):
        request = self.queue.pop()
        if request:
            self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
        return request

    def enqueue_request(self, request):
        if request.dont_filter:
            self.queue.push(request)
        elif not self.dupefilter.request_seen(request):
            self.queue.push(request)
        else:
            return False
        self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        return True

    def has_pending_requests(self):
        return len(self.queue) > 0

    def __del__(self):
        reason = 'KeyBoard ctrl+c to stop'
        if not self.persist:
            self.queue.close(reason)
            self.dupefilter.close(reason)

