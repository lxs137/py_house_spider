def robust_crawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('抓取出错：', e)
            return None
    return decorate


def robust_check(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('发生错误:', e)
            return False
    return decorate
