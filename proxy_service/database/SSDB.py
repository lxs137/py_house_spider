from proxy_service.database.ssdb_helper import Client


class SSDBManager(object):
    def __init__(self, host='127.0.0.1', port=8888):
        try:
            self.c = Client(host=host, port=port)
        except:
            print('SSDB connect error.')

    def create_list(self, name, list_data):
        list_size = self.c.qsize(name)
        list_data = list_data or []
        for item in list_data:
            self.c.qpush(name, item)
        self.c.qpop(name, list_size)

    def clear_list(self, name):
        self.c.qclear(name)

    def insert_list_item(self, name, item):
        self.c.qpush_front(name, item)

    def get_list(self, name):
        size = self.c.qsize(name)
        li_bytes = self.c.qrange(name, 0, size)
        li_str = []
        for li_item in li_bytes:
            # type(li_item) = bytes
            li_str.append(li_item.decode())
        return li_str

    def get_list_front(self, name):
        if self.c.qfront(name) != None:
            item = self.c.qpop_front(name)
            self.c.qpush_back(name, item)
            return item.decode()
        else:
            return None

    def incre_hashmap_item(self, name, item, increment, base):
        if not self.c.hexists(name, item):
            self.c.hset(name, item, base)
        self.c.hincr(name, item, increment)

    def clear_hashmap(self, name):
        self.c.hclear(name)

    def get_hashmap_key(self, name, value_min):
        kv_list = self.c.hgetall(name)
        kv_list_size = len(kv_list)
        key_list = []
        for i in range(kv_list_size):
            if i % 2 == 0:
                value = kv_list[i+1]
                if value >= value_min:
                    key_list.append(kv_list[i])
            else:
                continue
        return key_list

    def close_connect(self):
        self.c.disconnect()

    def __del__(self):
        self.close_connect()


if __name__ == '__main__':
    c = Client(host='127.0.0.1', port=8888)
    map = c.hgetall('connect_error_num')
    print(type(map))