from queuelib.pqueue import PriorityQueue
from redis import StrictRedis
class RedisRequestQueue(PriorityQueue):
    def __init__(self, host, port, password):
        self.server = StrictRedis(host=host, port=port, password=password)
