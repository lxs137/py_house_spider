from sf_house_spider.items import CommunityItem
from sf_house_spider.Pipelines.mysql import MySQLConnectorSF
from datetime import date
import re
import functools
from twisted.internet.threads import deferToThread

class SFDataBasePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, CommunityItem):
            info_dict = {}
            url = item['page_url']
            info_dict['code'] = 'sf_'+url[url.find('http://')+7:url.find('.fang')]
            info_dict['name'] = item['name']
            info_dict['region'] = item['region']
            info_dict['page_url'] = item['page_url']
            info_dict['sell_url'] = item['sell_url']
            info_dict['rent_url'] = item['rent_url']
            info_dict['record_url'] = item['record_url']
            info_dict['price_cur'] = item['price_cur']
            info_dict['ratio_month'] = item['ratio_month']
            info_dict['address'] = item['address']
            info_dict['community_feature'] = item.get('community_feature')
            info_dict['property'] = item.get('property')
            info_dict['manage_type'] = item.get('manage_type')

            if item.get('done_time'):
                date_str = item['done_time'].split('-')
                info_dict['done_time'] = date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
            else:
                info_dict['done_time'] = None
            info_dict['build_company'] = item.get('build_company')
            info_dict['building_type'] = item.get('building_type')
            info_dict['building_area'] = self.parse_number(item.get('building_area'), False)
            info_dict['cover_area'] = self.parse_number(item.get('cover_area'), False)
            info_dict['house_num_cur'] = self.parse_number(item.get('house_num_cur'), False)
            info_dict['house_num_sum'] = self.parse_number(item.get('house_num_sum'), False)
            info_dict['green_rate'] = self.parse_number(item.get('green_rate'), True)
            info_dict['volum_rate'] = self.parse_number(item.get('volum_rate'), True)
            info_dict['construction_rate'] = None
            info_dict['manage_price'] = self.parse_number(item.get('manage_price'), True)
            info_dict['info_add'] = item.get('info_add')
            info_dict['water_price'] = item.get('water_price')
            info_dict['electric_price'] = item.get('electric_price')
            info_dict['gas_price'] = item.get('gas_price')
            info_dict['network'] = item.get('network')
            info_dict['elector'] = item.get('elector')
            info_dict['security'] = item.get('security')
            info_dict['sanitation'] = item.get('sanitation')
            info_dict['parking'] = item.get('parking')
            info_dict['metro'] = item.get('metro')
            info_dict['bus'] = item.get('bus')
            info_dict['car'] = item.get('car')
            info_dict['kindergarten'] = item.get('kindergarten')
            info_dict['school'] = item.get('school')
            info_dict['university'] = item.get('university')
            info_dict['shop_mall'] = item.get('shop_mall')
            info_dict['hospital'] = item.get('hospital')
            info_dict['post_office'] = item.get('post_office')
            info_dict['bank'] = item.get('bank')
            info_dict['other_facility'] = item.get('other_facility')

            info_dict['property_company'] = None
            info_dict['building_num_sum'] = None
            insert_func = functools.partial(MySQLConnectorSF.insert_community_info, info_dict)
            deferToThread(insert_func)
            # MySQLConnectorSF.insert_community_info(info_dict)
            return item

    def parse_number(self, str, returnFloat):
        if str:
            match_object = re.search('[0-9|\.|-]+', str)
            if match_object:
                if returnFloat:
                    return float(match_object.group())
                else:
                    return int(float(match_object.group()))
            else:
                return None
        else:
            return None
