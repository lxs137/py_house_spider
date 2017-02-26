
def thread_safe_sql(func):
    def decorator(cls, *args, **kwargs):
        cls.lock.acquire()
        result = func(cls, *args, **kwargs)
        cls.lock.release()
        return result
    return decorator