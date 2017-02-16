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


def my_log(log_name):
    import sys

    def real_decorate(func):
        def output_decorate(*args, **kwargs):
            if sys.stdout.name == '<stdout>':
                console_stdout = sys.stdout
                f_log = open(log_name, 'a+')
                sys.stdout = f_log
                func_return = func(*args, **kwargs)
                sys.stdout = console_stdout
                f_log.close()
                return func_return
            else:
                return func(*args, **kwargs)
        return output_decorate
    return real_decorate


