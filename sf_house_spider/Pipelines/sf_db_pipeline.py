from sf_house_spider.items import CommunityItem
from sf_house_spider.Pipelines.mysql import MySQLConnectorSF
from datetime import date
import re

class SFDataBasePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, CommunityItem):
            info_dict = {}
            info_dict['name'] = item['name']
            info_dict['region'] = item['region']
            info_dict['page_url'] = item['page_url']
            info_dict['price_cur'] = item['price_cur']
            info_dict['ratio_month'] = item['ratio_month']
            info_dict['address'] = item['address']
            info_dict['community_feature'] = item['community_feature']
            info_dict['property'] = item['property']
            info_dict['manage_type'] = item['manage_type']

            if item['done_time']:
                date_str = item['done_time'].split('-')
                info_dict['done_time'] = date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
            else:
                info_dict['done_time'] = None
            info_dict['build_company'] = item['build_company']
            info_dict['building_type'] = item['building_type']
            info_dict['building_area'] = self.parse_number(item['building_area'], False)
            info_dict['cover_area'] = self.parse_number(item['cover_area'], False)
            info_dict['house_num_cur'] = self.parse_number(item['house_num_cur'], False)
            info_dict['house_num_sum'] = self.parse_number(item['house_num_sum'], False)
            info_dict['green_rate'] = self.parse_number(item['green_rate'], True)
            info_dict['volum_rate'] = self.parse_number(item['volum_rate'], True)
            info_dict['manage_price'] = self.parse_number(item['manage_price'], True)
            info_dict['info_add'] = item['info_add']
            info_dict['water_price'] = item['water_price']
            info_dict['electric_price'] = item['electric_price']
            info_dict['gas_price'] = item['gas_price']
            info_dict['network'] = item['network']
            info_dict['elector'] = item['elector']
            info_dict['security'] = item['security']
            info_dict['sanitation'] = item['sanitation']
            info_dict['parking'] = item['parking']
            info_dict['metro'] = item['metro']
            info_dict['bus'] = item['bus']
            info_dict['car'] = item['car']
            info_dict['kindergarten'] = item['kindergarten']
            info_dict['school'] = item['school']
            info_dict['university'] = item['university']
            info_dict['shop_mall'] = item['shop_mall']
            info_dict['hospital'] = item['hospital']
            info_dict['post_office'] = item['post_office']
            info_dict['bank'] = item['bank']
            info_dict['other_facility'] = item['other_facility']
            MySQLConnectorSF.insert_community_info(info_dict)
            return item

    def parse_number(self, str, returnFloat):
        if str:
            match_object = re.match('[0-9|\.|-]+', str)
            if match_object:
                if returnFloat:
                    return float(match_object.group())
                else:
                    return int(float(match_object.group()))
            else:
                return None
        else:
            return None
