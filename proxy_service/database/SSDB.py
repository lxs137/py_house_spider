from proxy_service.database.ssdb_helper import Client
class SSDBManager(object):
    try:
        c = Client(host='127.0.0.1', port=8888)
    except:
        print('SSDB connect error.')

    @classmethod
    def create_list(cls, name, li):
        cls.c.qclear(name)
        for item in li:
            cls.c.qpush(item)

    @classmethod
    def insert_list_item(cls, name, item):
        cls.c.qpush_front(name, item)

    @classmethod
    def get_list(cls, name):
        size = cls.c.qsize(name)
        li = cls.c.qrange(name, 0, size)
        return li

    @classmethod
    def get_list_front(cls, name):
        if cls.c.qfront(name) != None:
            item = cls.c.qpop_front(name)
            cls.c.qpush_back(name, item)
            return item
        else:
            return None

    @classmethod
    def insert_test(cls):
        print('insert')

    @classmethod
    def close_connect(cls):
        cls.c.disconnect()


if __name__ == '__main__':
    c = Client(host='127.0.0.1', port=8888)
    li = c.qfront('li_test')
    str = str(li)
    print(str)