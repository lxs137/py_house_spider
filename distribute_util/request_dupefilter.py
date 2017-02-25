from scrapy.utils.request import request_fingerprint
from scrapy.dupefilters import BaseDupeFilter
from redis import Redis


class RedisDupeFilter(BaseDupeFilter):
    def __init__(self, settings, dupefilter_key):
        self.server = Redis(host=settings.get('REDIS_HOST', 'localhost'),
                            port=settings.get('REDIS_PORT', 6379),
                            password=settings.get('REDIS_PASSWORD', None))
        self.key = dupefilter_key

    def close(self, reason):
        self.server.delete(self.key)

    def request_seen(self, request):
        # 判断request是否已经被请求过
        fingerprint = request_fingerprint(request)
        seen = self.server.sismember(self.key, fingerprint)
        if seen:
            return True
        else:
            self.server.sadd(self.key, fingerprint)
            return False
