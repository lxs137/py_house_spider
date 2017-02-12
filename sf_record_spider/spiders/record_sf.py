import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup, NavigableString
import re
from sf_record_spider.Pipelines.mysql import MySQLConnectorSF
from sf_record_spider.items import SellItem, RentItem, RecordSellItem, RecordRentItem
class RecordSpider(scrapy.Spider):
    name = 'sf_record_spider'
    pay_params_url = 'http://dai.fangtx.com/new/ReferenceYueG/index.html'
    month_pay_params = {'year_num': 30, 'rate': ['0.0475', '0.049', '0.0275', '0.0325'], 'cheng_num': 7}
    def start_requests(self):
        MySQLConnectorSF.create_tables()
        sql_list = MySQLConnectorSF.select_community_url()
        yield Request(self.pay_params_url, callback=self.parse_pay_params)
        for sql_tuple in sql_list:
            sell_url = sql_tuple[0]
            rent_url = sql_tuple[1]
            record_url = sql_tuple[2]
            community_id = sql_tuple[3]
            record_sell_url = record_url + '-p11-t11/'
            record_rent_url = record_url + '-p11-t12/'
            yield Request(sell_url, callback=self.sell_page_list,
                          meta={'base_url': sell_url, 'community_id': community_id})
            yield Request(rent_url, callback=self.rent_page_list,
                          meta={'base_url': rent_url, 'community_id': community_id})
            yield Request(record_sell_url, callback=self.record_sell_page_list,
                          meta={'base_url': record_url, 'community_id': community_id})
            yield Request(record_rent_url, callback=self.record_rent_page_list,
                          meta={'base_url': record_url, 'community_id': community_id})

    def sell_page_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        page_str = soup.find('div', attrs={'class': 'frpageChange floatl'})\
            .find('span', attrs={'class': 'floatr ml10'}).get_text()
        max_page = int(page_str[page_str.find('/')+1:])
        base_url = response.meta['base_url']
        for i in range(1, max_page+1):
            page_url = base_url+'list/-h332-i3'+str(i)+'/'
            yield Request(page_url, callback=self.parse_sell_list
                          , meta={'community_id': response.meta['community_id']}, dont_filter=True)

    def parse_sell_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        sell_list = soup.find('div', attrs={'class': 'rentListwrap fangListwrap'})\
            .find_all('div', attrs={'class': 'fangList'})
        meta_dict = {}
        meta_dict['community_id'] = response.meta['community_id']
        for item in sell_list:
            meta_dict['priceAll'] = int(float(item.find_all('ul', attrs={'class': 'Price'})[1].find('span').get_text()))
            price_str = item.find_all('ul', attrs={'class': 'Price'})[1].find('li', attrs={'class': 'update'}).get_text()
            price_str = ''.join(price_str.split())
            meta_dict['pricePer'] = int(float(re.match('[0-9]+', price_str).group()))
            area_str = item.find('ul', attrs={'class': 'Price area'}).get_text()
            area_str = ''.join(area_str.split())
            meta_dict['area'] = int(float(re.match('[0-9]+', area_str).group()))
            url = item.find('dl', attrs={'class': 'clearfix'})\
                .find('p', attrs={'class': 'fangTitle'}).find('a')['href']
            yield Request(url, callback=self.parse_sell_info, meta=meta_dict)

    def parse_sell_info(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        sell_item = SellItem()
        sell_item['community_id'] = response.meta['community_id']
        title_str = soup.find('div', attrs={'class': 'mainBoxL'})\
            .find('div', attrs={'class': 'title'}).find('p').get_text()
        title_str = ''.join(title_str.split())
        code_str = re.search('房源编号：[0-9]+', title_str).group()
        sell_item['code'] = 'sf_'+code_str[code_str.find('：')+1:]
        time_str = re.search('发布时间：[0-9|/|-]+', title_str).group()
        sell_item['release_time'] = time_str[time_str.find('：')+1:]
        sell_item['price_all'] = response.meta['priceAll']
        sell_item['price_per'] = response.meta['pricePer']
        sell_item['area_build'] = response.meta['area']
        info_dl = soup.find('div', attrs={'class': 'mainBoxL'})\
            .find('div', attrs={'class': 'houseInfor'})\
            .find('div', attrs={'class': 'inforTxt'}).find_all('dl')
        dd_list = []
        for dl in info_dl:
            dd_list.extend(dl.find_all('dd'))
            dd_list.extend(dl.find_all('dt'))
        for dd_item in dd_list:
            dd_str = dd_item.get_text()
            dd_str = ''.join(dd_str.split())
            if dd_str.find('参考首付') != -1:
                sell_item['first_pay'] = int(float(re.search('[0-9]+', dd_str).group()))
            elif dd_str.find('参考月供') != -1:
                sell_item['month_pay'] = self.calculate_month_pay(sell_item['price_all'])
            elif dd_str.find('装修') != -1:
                sell_item['decoration'] = dd_str[dd_str.find('：')+1:]
            elif dd_str.find('户型') != -1:
                sell_item['house_model'] = dd_str[dd_str.find('：')+1:]
            elif dd_str.find('结构') != -1:
                sell_item['house_structure'] = dd_str[dd_str.find('：')+1:]
            elif dd_str.find('住宅类别') != -1:
                sell_item['house_type'] = dd_str[dd_str.find('：')+1:]
            elif dd_str.find('产权性质') != -1:
                sell_item['property_type'] = dd_str[dd_str.find('：')+1:]
            elif dd_str.find('楼层') != -1:
                sell_item['floor'] = dd_str[dd_str.find('：')+1:]
            elif dd_str.find('朝向') != -1:
                sell_item['direction'] = dd_str[dd_str.find('：')+1:]
            elif dd_str.find('年代') != -1:
                sell_item['build_time'] = int(re.search('[0-9]+', dd_str).group())
        return sell_item

    def rent_page_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        page_str = soup.find('div', attrs={'class': 'frpageChange floatr'})\
            .find('span', attrs={'class': 'floatr'}).get_text()
        max_page = int(page_str[page_str.find('/')+1:])
        base_url = response.meta['base_url']
        for i in range(1, max_page+1):
            page_url = base_url+'list/h322-i3'+str(i)+'/'
            yield Request(page_url, callback=self.parse_rent_list
                          , meta={'community_id': response.meta['community_id']}, dont_filter=True)
        pass

    def parse_rent_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        rent_list = soup.find('div', attrs={'class': 'rentListwrap fangListwrap'})\
            .find_all('div', attrs={'class': 'fangList'})
        for item in rent_list:
            url = item.find('dl', attrs={'class': 'clearfix'})\
                .find('p', attrs={'class': 'fangTitle'}).find('a')['href']
            yield Request(url, callback=self.parse_rent_info, meta={'community_id': response.meta['community_id']})

    def parse_rent_info(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        rent_item = RentItem()
        rent_item['community_id'] = response.meta['community_id']
        title_tag_list = soup.find('div', attrs={'class': 'h1-tit'})\
            .find('p', attrs={'class': 'gray9'}).find_all('span')
        code_str = title_tag_list[0].get_text()
        code_str = ''.join(code_str.split())
        rent_item['code'] = 'sf_'+re.search(r'[0-9]+', code_str).group()
        update_str = title_tag_list[1].get_text()
        update_str = (update_str.split())[0]
        rent_item['update_time'] = update_str[update_str.find('：')+1:]
        info_list = soup.find('ul', attrs={'class': 'house-info'}).find_all('li')
        for info_tag in info_list:
            tag_name = info_tag.find('span', attrs={'class': 'info-tit'}).get_text()
            tag_name = ''.join(tag_name.split())
            tag_content = info_tag.get_text()
            tag_content = ''.join(tag_content.split())
            tag_content = tag_content[tag_content.find('：')+1:]
            if tag_name.find('租金') != -1:
                rent_item['price'] = int(float(re.search(r'[0-9]+元', tag_content).group()[:-1]))
                rent_item['pay_type'] = re.search('\[.*\]', tag_content).group()[1:-1]
                try:
                    rent_item['rate'] = float((re.search(r'[0-9|.|-]+%', tag_content).group())[:-1])
                except:
                    rent_item['rate'] = 0.00
            elif tag_name.find('房屋概况') != -1:
                content_list = tag_content.split('|')
                for content in content_list:
                    if re.search('[东|南|西|北]+', content) != None:
                        rent_item['direction'] = content
                    elif content.find('装修') != -1:
                        rent_item['decoration'] = content
                    elif content.find('层') != -1:
                        rent_item['floor'] = content
                    elif content.find('�O') != -1:
                        rent_item['area_build'] = int(float(re.search('[0-9]+', content).group()))
                    elif re.search('[0-9]+室', content) != None:
                        rent_item['house_model'] = content
                    else:
                        rent_item['house_type'] = content
        js_text = soup.find('script').get_text()
        support_list = re.search("'.*'", re.search(r'var peitao.*;', js_text).group()).group()[1:-1].split(',')
        support_attr_list = ['support_bed', 'support_furniture', 'support_gas', 'support_warm',
                           'support_network', 'support_tv', 'support_condition', 'support_fridge',
                           'support_wash', 'support_water']
        support_attr_dict = {'support_bed': '床', 'support_furniture': '家具', 'support_gas': '煤气/天然气',
                             'support_warm': '暖气', 'support_network': '宽带', 'support_tv': '有线电视',
                             'support_condition': '空调', 'support_fridge': '冰箱',
                             'support_wash': '洗衣机', 'support_water': '热水器'}
        for support_attr in support_attr_list:
            if support_list.count(support_attr_dict[support_attr]) != 0:
                rent_item[support_attr] = 1
            else:
                rent_item[support_attr] = 0
        yield rent_item

    def record_rent_page_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        page_url = soup.find('div', attrs={'class': 'detailTitle'})\
            .find('div', attrs={'class': 'frpageChange'})\
            .find('span', attrs={'class': 'ml10'}).get_text()
        max_page = int(page_url[page_url.find('/')+1:])
        for i in range(1, max_page+1):
            url = response.meta['base_url']+'-p1'+str(i)+'-t12/'
            yield Request(url, callback=self.parse_record_rent_list
                          , meta={'community_id': response.meta['community_id']}, dont_filter=True)

    def record_sell_page_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        page_url = soup.find('div', attrs={'class': 'detailTitle'})\
            .find('div', attrs={'class': 'frpageChange'})\
            .find('span', attrs={'class': 'ml10'}).get_text()
        max_page = int(page_url[page_url.find('/')+1:])
        for i in range(1, max_page+1):
            url = response.meta['base_url']+'-p1'+str(i)+'-t11/'
            yield Request(url, callback=self.parse_record_sell_list
                          , meta={'community_id': response.meta['community_id']}, dont_filter=True)

    def parse_record_sell_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        tr_list = soup.find('div', attrs={'class': 'tableWrap'})\
            .find('table').find('tbody').find_all('tr')
        if tr_list[0].find('th') != None:
            del tr_list[0]
        for tr_item in tr_list:
            record_sell_item = RecordSellItem()
            record_sell_item['community_id'] = response.meta['community_id']
            td_first = tr_item.find('div', attrs={'class': 'hspro'}).contents
            td_first_str = []
            for td_first_item in td_first:
                if isinstance(td_first_item, NavigableString):
                    continue
                td_first_str.append(''.join(td_first_item.get_text().split()))
            for first_str in td_first_str:
                if re.search('[东|南|西|北]+', first_str) != None:
                    record_sell_item['direction'] = first_str
                elif first_str.find('层') != -1:
                    record_sell_item['floor'] = first_str
                elif re.search('[0-9]+室', first_str) != None:
                    record_sell_item['house_model'] = first_str
            td_list = tr_item.find_all('td')
            if td_list[0]['class'].count('firsttd') != 0:
                del td_list[0]
            for td_item in td_list:
                item_str = td_item.get_text()
                item_str = ''.join(item_str.split())
                if re.search('[0-9|.]+�O', item_str) != None:
                    record_sell_item['area_build'] = int(float(re.search('[0-9|.]+', item_str).group()))
                elif re.search('[0-9]+-[0-9]+-[0-9]+', item_str) != None:
                    record_sell_item['sell_time'] = item_str
                elif re.search('[0-9|.]+万', item_str) != None:
                    record_sell_item['price_all'] = int(float(re.search('[0-9|.]+', item_str).group()))
                elif re.search('[0-9|.]+元/', item_str) != None:
                    record_sell_item['price_per'] = int(float(re.search('[0-9|.]+', item_str).group()))
            yield record_sell_item

    def parse_record_rent_list(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        tr_list = soup.find('div', attrs={'class': 'tableWrap'})\
            .find('div', attrs={'class': 'dealRent'}).find('tbody').find_all('tr')
        del tr_list[0]
        for tr_item in tr_list:
            if ''.join(tr_item.get_text().split()) == '':
                continue
            else:
                record_rent_item = RecordRentItem()
                record_rent_item['community_id'] = response.meta['community_id']
                td_list = tr_item.find_all('td')
                for td_item in td_list:
                    td_str = td_item.get_text()
                    td_str = ''.join(td_str.split())
                    if re.search('[0-9]+-[0-9]+-[0-9]+', td_str) != None:
                        record_rent_item['sell_time'] = td_str
                    elif re.search('[0-9]+元/月', td_str) != None:
                        record_rent_item['price'] = int(re.search('[0-9]+', td_str).group())
                    elif re.search('[0-9]+室', td_str) != None:
                        record_rent_item['house_model'] = td_str
                    elif re.search('[0-9|.]+�O', td_str) != None:
                        record_rent_item['area_build'] = int(float(re.search('[0-9]+', td_str).group()))
                    elif td_str.find('层') != -1:
                        record_rent_item['floor'] = td_str
                    elif re.search('[东|南|西|北]+', td_str) != None:
                        record_rent_item['direction'] = td_str
                yield record_rent_item

    def parse_pay_params(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        self.month_pay_params['cheng_num'] = int(soup.find('select', id='ChengNum')\
            .find('option', attrs={'selected': 'selected'})['value'])
        self.month_pay_params['year_num'] = int(soup.find('select', id='YearNum')\
            .find('option', attrs={'selected': 'selected'})['value'])
        self.month_pay_params['rate'] = (soup.find('select', id='Rate')\
            .find('option', attrs={'selected': 'selected'})['value']).split('|')

    # year_num:贷款年份
    # rate:利率
    # cheng_num:按揭成数
    def calculate_month_pay(self, house_money):
        year_num = self.month_pay_params['year_num']
        rate = self.month_pay_params['rate']
        cheng_num = self.month_pay_params['cheng_num']
        if year_num <= 5:
            rate_use = float(rate[0])
        else:
            rate_use = float(rate[1])
        a = house_money * cheng_num * 1000 * rate_use / 12
        b = pow((1 + rate_use / 12), year_num * 12)
        month_pay = (a * b) / (b - 1)
        return round(month_pay, 2)
