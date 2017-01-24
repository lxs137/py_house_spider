from bs4 import BeautifulSoup
from scrapy.http import Request
import scrapy

class CommunitySpider(scrapy.Spider):
    name = 'community_spider'
    # 限制爬取的域名范围
    allowed_domains = ['esf.nanjing.fang.com']
    base_url = 'http://esf.nanjing.fang.com/housing/'
    community = [u'鼓楼', u'江宁', u'浦口', u'玄武', u'建邺', u'栖霞', u'雨花',
                 u'秦淮', u'六合', u'溧水', u'高淳', u'南京周边']
    community_code = {u'鼓楼': '265', u'江宁': '268', u'浦口': '270', u'玄武': '264',
                      u'建邺': '267', u'栖霞': '271', u'雨花': '272', u'秦淮': '263',
                      u'六合': '269', u'溧水': '274', u'高淳': '275', u'南京周边': '13046'}

    def start_requests(self):
        for one_community in self.community:
            code = self.community_code[one_community]
            region_url = self.base_url + code + '__0_0_0_0_1_0_0/'
            yield Request(region_url, self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        page_str = soup.find('span', attrs={'class': 'fy_text'}).get_text()
        max_page = int(page_str[(page_str.find('/')+1):])
        for i in range(1, max_page+1):
            region_page_url = str(response.url).replace('1_0_0', str(i)+'_0_0')
            yield Request(region_page_url, callback=self.get_community_url)

    def get_community_url(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        community_list = soup.find_all('div', attrs={'class': 'list rel'})
        for community_item in community_list:
            community_url = community_item.find('a', attrs={'class': 'plotTit'})['href']
            community_type = community_item.find('span', attrs={'class': 'plotFangType'}).get_text()
            if community_url.find('http://') != -1:
                if community_type == '住宅' or community_type == '别墅':
                    print(community_url, ' Type1')
                elif community_type == '商铺' or community_type == '写字楼':
                    print(community_url, ' Type2')
            # yield Request(community_url)