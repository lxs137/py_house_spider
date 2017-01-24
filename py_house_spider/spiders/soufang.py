from bs4 import BeautifulSoup
import scrapy

class CommunitySpider(scrapy.Spider):
    name = 'community_spider'
    # 限制爬取的域名范围
    allowed_domains = ['esf.nanjing.fang.com']
    start_urls = ['http://esf.nanjing.fang.com/housing/268__0_0_0_0_1_0_0/']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        print(soup.find('title'))
        # print(response.body)


