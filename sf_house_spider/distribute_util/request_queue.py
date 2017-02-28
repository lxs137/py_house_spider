from scrapy.utils.reqser import request_from_dict, request_to_dict
import pickle
from redis import Redis


class RedisRequestQueue(object):

    def __init__(self, server, spider, queue_key):
        self.server = server
        self.spider = spider
        self.key = queue_key

    def _decode_request(self, request_data):
        return request_from_dict(pickle.loads(request_data), self.spider)

    def _encode_request(self, request):
        # protocol为负数代表使用HIGEST_PROTOCOL
        return pickle.dumps(request_to_dict(request, self.spider), protocol=-1)

    def __len__(self):
        return self.server.zcard(self.key)

    def close(self, reason):
        self.server.delete(self.key)

    def pop(self):
        pipe = self.server.pipeline()
        # 保证接下来的操作作为一个事务进行执行
        pipe.multi()
        pipe.zrange(self.key, 0, 0)
        pipe.zremrangebyrank(self.key, 0, 0)
        value, count = pipe.execute()
        if value:
            return self._decode_request(value[0])

    def push(self, request):
        request_data = self._encode_request(request)
        # 对request来说,priority越大优先级越高,
        # 但对于redis的有序集合来说,默认情况下:score分数越低优先级越高
        # 因此将request.priority取负数作为member的score
        self.server.zadd(self.key, request_data, -request.priority)


