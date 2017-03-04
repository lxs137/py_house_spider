# -*- coding: utf-8 -*-

# Scrapy settings for py_house project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sf_house_spider'

SPIDER_MODULES = ['sf_house_spider.spiders']
NEWSPIDER_MODULE = 'sf_house_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'py_house (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#     'myproject.middlewares.SpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    'sf_house_spider.Download.retry.RetryMiddleware': 500,
    'sf_house_spider.Download.proxy.ProxyMiddleware': 100,
    'sf_house_spider.Download.user_agent.UserAgentMiddleware': 400,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'py_house.pipelines.SomePipeline': 300,
    'sf_house_spider.Pipelines.sf_db_pipeline.SFDataBasePipeline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_FILE = '/home/lxs/spider_log/scrapy_community.log'
LOG_LEVEL = 'INFO'

# Twisted线程池同时允许的线程数量
REACTOR_THREADPOOL_MAXSIZE = 20


MYSQL_HOSTS = '118.89.107.231'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '1q2w3e4r'
MYSQL_PORT = '3306'
MYSQL_DB_SF = 'house_sf'

PROXY_SERVICE_ADDRESS = 'http://118.89.107.231:80/'
PROXY_MAX_USE = '30'
DEFAULT_PROXY = '222.33.192.238:8118'

REDIS_HOST = '123.206.189.122'
REDIS_PORT = 9736
REDIS_PASSWORD = '1q2w3e4r'

SCHEDULER_PERSIST = False
SCHEDULER = 'sf_house_spider.distribute_util.request_scheduler.RedisScheduler'

