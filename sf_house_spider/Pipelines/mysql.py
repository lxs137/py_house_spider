import mysql.connector
from mysql.connector import errorcode
from sf_house_spider import settings
from sf_house_spider.items import CommunityItem

class MySQLConnectorSF(object):
    try:
        cnx = mysql.connector.connect(user=settings.MYSQL_USER,
                                      password=settings.MYSQL_PASSWORD,
                                      host=settings.MYSQL_HOSTS,
                                      database=settings.MYSQL_DB_SF)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with your user name or password.')
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist.')
        else:
            print(error)
    else:
        cursor = cnx.cursor(buffered=True)

    @classmethod
    def insert_community_info(cls, info_dict):
        insert_command = 'INSERT INTO community_info('\
                         'name,page_url,price_cur,ratio_month,address,' \
                         'character,region,property,manage_type,done_time,' \
                         'build_company,building_type,building_area,cover_area,' \
                         'house_num_cur,house_num_sum,green_rate,volum_rate,' \
                         'manage_price,info_add,water_price,electric_price,gas_price,' \
                         'network,elector,security,sanitation,parking,metro,bus,car,' \
                         'kindergarten,school,university,shop_mall,hospital,post_office,' \
                         'bank,other_facility)'\
                         'VALUES ()'
        pass
    pass