from bs4 import BeautifulSoup
from scrapy.http import Request
import scrapy
from py_house_spider.items import URLItem
from py_house_spider.items import CommunityItem

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
    community_url_num = {u'鼓楼': 0, u'江宁': 0, u'浦口': 0, u'玄武': 0, u'建邺': 0, u'栖霞': 0,
                         u'雨花': 0, u'秦淮': 0, u'六合': 0, u'溧水': 0, u'高淳': 0, u'南京周边': 0}


    def start_requests(self):
        for one_community in self.community:
            code = self.community_code[one_community]
            region_url = self.base_url + code + '__0_0_0_0_1_0_0/'
            yield Request(region_url, callback=self.parse, meta={'region': one_community})

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        page_str = soup.find('span', attrs={'class': 'fy_text'}).get_text()
        max_page = int(page_str[(page_str.find('/')+1):])
        for i in range(1, max_page+1):
            region_page_url = str(response.url).replace('1_0_0', str(i)+'_0_0')
            yield Request(region_page_url, callback=self.get_community_url,
                          meta={'region': response.meta['region']})

    def get_community_url(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        community_list = soup.find_all(attrs={'class': 'plotListwrap'})
        for community_item in community_list:
            community_url = community_item.find('a', attrs={'class': 'plotTit'})['href']
            community_type = community_item.find('span', attrs={'class': 'plotFangType'}).get_text()
            if community_url.find('http://') != -1:
                if community_type == u'住宅' or community_type == u'别墅':

                    # Get priceAverage and ratio
                    meta_request = {'region': response.meta['region']}
                    price_tag = community_item.find('p', attrs={'class': 'priceAverage'})
                    ratio_tag = community_item.find('p', attrs={'class': 'ratio'})
                    if price_tag is None:
                        meta_request['priceAverage'] = 0
                        meta_request['ratio'] = 0.00
                    else:
                        meta_request['priceAverage'] = int(price_tag.find('span').get_text())
                        if ratio_tag is None:
                            meta_request['ratio'] = 0.00
                        else:
                            ratio_tag =ratio_tag.find('span')
                            class_list = ratio_tag['class']
                            if class_list.count('red') == 1:
                                meta_request['ratio'] = float((ratio_tag.find('span').get_text())[1:-1])
                            elif class_list.count('green') == 1:
                                meta_request['ratio'] = -1*float((ratio_tag.find('span').get_text())[1:-1])

                    community_info_url = community_url[:community_url.find('.com')] +'.com/xiangqing/'
                    yield Request(community_info_url, callback=self.get_community_info,
                                  meta=meta_request)
                elif community_type == u'商铺' or community_type == u'写字楼':
                    pass

    def get_community_info(self, response):
        info = CommunityItem()
        soup = BeautifulSoup(response.body, 'lxml')
        title_str = str(soup.find('title').get_text())
        info['name'] = soup.find('a', attrs={'class': 'tt'}).get_text()
        info['page_url'] = response.url
        info['price_cur'] = response.meta['priceAverage']
        info['ratio_month'] = response.meta['ratio']
        box_list = soup.find_all('div', attrs={'class': 'box'})

        pass
