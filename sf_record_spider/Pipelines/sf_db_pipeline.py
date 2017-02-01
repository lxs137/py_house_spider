from sf_record_spider.Pipelines.mysql import MySQLConnectorSF
from scrapy.exceptions import DropItem
import re
from datetime import date
class SFDataBasePipeline(object):

    def process_item(self, item, spider):
        insert_dict = {}
        if item['community_id']:
            insert_dict['code'] = item['code']

            time_str = item['release_time']
            time_str = ''.join(time_str.split())
            time_str = re.sub('[^0-9]', '-', time_str)
            time_list = time_str.split('-')
            insert_dict['release_time'] = date(int(time_list[0]), int(time_list[1]), int(time_list[2]))

            insert_dict['price_all'] = item['price_all']
            insert_dict['price_per'] = item['price_per']
            insert_dict['first_pay'] = item.get('first_pay')
            insert_dict['month_pay'] = item.get('month_pay')
            insert_dict['floor'] = item.get('floor')
            insert_dict['area_build'] = item['area_build']
            insert_dict['direction'] = item.get('direction')
            insert_dict['decoration'] = item.get('decoration')
            insert_dict['house_model'] = item.get('house_model')
            insert_dict['build_time'] = item.get('build_time')
            insert_dict['house_structure'] = item.get('house_structure')
            insert_dict['house_type'] = item.get('house_type')
            insert_dict['property_type'] = item.get('property_type')
            MySQLConnectorSF.insert_sell_info(insert_dict, item['community_id'])
        else:
            raise DropItem('Item: Missing community_info_id.')
