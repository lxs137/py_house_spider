from proxy_service.database.ssdb_helper import Client


class SSDBManager(object):
    def __init__(self, host='127.0.0.1', port=8888):
        try:
            self.c = Client(host=host, port=port)
        except:
            print('SSDB connect error.')

    def create_list(self, name, list_data):
        self.c.qclear(name)
        for item in list_data:
            self.c.qpush(name, item)

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

    def close_connect(self):
        self.c.disconnect()


if __name__ == '__main__':
    c = Client(host='127.0.0.1', port=8888)
    c.qclear('no_list')
    print('clear')