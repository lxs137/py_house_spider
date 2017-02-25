from scrapy.utils.reqser import request_from_dict, request_to_dict
import pickle
from redis import Redis


class RedisRequestQueue(object):

    def __init__(self, settings, spider, queue_key):
        self.server = Redis(host=settings.get('REDIS_HOST', 'localhost'),
                            port=settings.get('REDIS_PORT', 6379),
                            password=settings.get('REDIS_PASSWORD', None))
        self.spider = spider
        self.key = queue_key

    def decode_request(self, request_data):
        return request_from_dict(pickle.loads(request_data), self.spider)

    def encode_request(self, request):
        # protocol为负数代表使用HIGEST_PROTOCOL
        return pickle.dumps(request_to_dict(request, self.spider), protocol=-1)

    def __len__(self):
        return self.server.zcard(self.key)

    def clear_queue(self):
        self.server.delete(self.key)

    def pop(self):
        pipe = self.server.pipeline()
        # 保证接下来的操作作为一个事务进行执行
        pipe.multi()
        pipe.zrange(self.key, 0, 0)
        pipe.zremrangebyrank(self.key, 0, 0)
        value, count = pipe.execute()
        if value:
            return self.decode_request(value[0])

    def push(self, request):
        request_data = self.encode_request(request)
        # 对request来说,priority越大优先级越高,
        # 但对于redis的有序集合来说,默认情况下:score分数越低优先级越高
        # 因此将request.priority取负数作为member的score
        add_item = {request_data: -request.priority}
        self.server.zadd(self.key, **add_item)

