def robust_crawl(func):
    def solve_exception(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('抓取出错：')
            print(e)
    return solve_exception
