import mysql.connector
from mysql.connector import errorcode
from sf_house_spider import settings

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
    def close_connect(cls):
        cls.cursor.close()
        cls.cnx.close()

    @classmethod
    def insert_community_info(cls, info_dict):
        insert_command = 'INSERT INTO community_info( \
                         name,page_url,sell_url,rent_url,record_url,price_cur,ratio_month,address, \
                         community_feature,region,property,manage_type,done_time, \
                         build_company,building_type,building_area,cover_area, \
                         house_num_cur,house_num_sum,green_rate,volum_rate, \
                         manage_price,info_add,water_price,electric_price,gas_price, \
                         network,elector,security,sanitation,parking,metro,bus,car, \
                         kindergarten,school,university,shop_mall,hospital,post_office, \
                         bank,other_facility)\
                         VALUES (%(name)s, %(page_url)s, %(sell_url)s, %(rent_url)s, %(record_url), s%(price_cur)s, %(ratio_month)s,\
                         %(address)s, %(community_feature)s, %(region)s, %(property)s,\
                         %(manage_type)s, %(done_time)s, %(build_company)s,\
                         %(building_type)s, %(building_area)s, %(cover_area)s,\
                         %(house_num_cur)s, %(house_num_sum)s, %(green_rate)s,\
                         %(volum_rate)s, %(manage_price)s, %(info_add)s, %(water_price)s,\
                         %(electric_price)s, %(gas_price)s, %(network)s, %(elector)s,\
                         %(security)s, %(sanitation)s, %(parking)s, %(metro)s, %(bus)s,\
                         %(car)s, %(kindergarten)s, %(school)s, %(university)s,\
                         %(shop_mall)s, %(hospital)s, %(post_office)s, %(bank)s,\
                         %(other_facility)s)'
        cls.cursor.execute(insert_command, info_dict)
        cls.cnx.commit()
        pass
    pass