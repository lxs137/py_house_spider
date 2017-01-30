import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
from sf_record_spider.Pipelines.mysql import MySQLConnectorSF
class RecordSpider(scrapy.Spider):
    name = 'sf_record_spider'
    def start_requests(self):
        url_list = MySQLConnectorSF.select_community_url()
        for url_tuple in url_list:
            sell_url = url_tuple[0]
            rent_url = url_tuple[1]
            record_url = url_tuple[2]
            yield Request(sell_url, callback=self.sell_page_list, meta={'base_url': sell_url})
            yield Request(rent_url, callback=self.rent_page_list, meta={'base_url': rent_url})
            yield Request(record_url, callback=self.record_page_list, meta={'base_url': record_url})
        pass

    def sell_page_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        page_str = soup.find('div', attrs={'class': 'frpageChange floatl'})\
            .find('span', attrs={'class': 'floatr ml10'}).get_text()
        max_page = int(page_str[page_str.find('/')+1:])
        base_url = response.meta['base_url']
        for i in range(1, max_page+1):
            page_url = base_url+'list/-h332-i3'+str(i)
            yield Request(page_url, callback=self.parse_sell_list)

    def parse_sell_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        sell_list = soup.find('div', attrs={'class': 'rentListwrap fangListwrap'})\
            .find_all('div', attrs={'class': 'fangList'})
        meta_dict = {}
        for item in sell_list:
            meta_dict['priceAll'] = int(item.find('ul', attrs={'class': 'Price'}).find('span').get_text())
            price_str = item.find('ul', attrs={'class': 'Price'}).find('li', attrs={'class': 'update'})
            meta_dict['pricePer'] = int(re.match('[0-9]+', price_str).group())
            area_str = item.find('ul', attrs={'class': 'Price area'}).get_text()
            meta_dict['area'] = int(re.match('[0-9]+', area_str).group())
            info_str = item.find('dl', attrs={'class': 'clearfix'}).find('p', attrs={'class': 'mt5'}).get_text()
            info_str = ''.join(info_str.split())
            info_list = info_str.split('|')
            meta_dict['model'] = info_list[0]
            meta_dict['floor'] = info_list[1]
            meta_dict['direction'] = info_list[2]
            meta_dict['buildTime'] = int(info_list[3][info_list[3].find('：')+1:])
            pass
        pass

    def rent_page_list(self):
        pass

    def parse_rent_list(self):
        pass

    def record_page_list(self):
        pass

    def parse_record_list(self):
        pass