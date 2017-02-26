import mysql.connector
from mysql.connector import errorcode
from sf_house_spider import settings
import time
import threading
from sf_house_spider.Pipelines.decorator_util import thread_safe_sql

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
        time_str = time.strftime('_%Y_%m_%d', time.localtime())
        lock = threading.Lock()

    @classmethod
    def create_table(cls):
        create_command = 'CREATE TABLE community_info'+cls.time_str+'(community_info_id'\
                         ' int NOT NULL PRIMARY KEY AUTO_INCREMENT,code varchar(100),name varchar(100),'\
                         'page_url varchar(255),sell_url varchar(255),rent_url varchar(255),'\
                         'record_url varchar(255),price_cur int,ratio_month float,'\
                         'address varchar(255),community_feature varchar(100),'\
                         'region varchar(100),property varchar(100),manage_type varchar(100),'\
                         'done_time date,build_company varchar(100),building_type varchar(100),'\
                         'building_area int,cover_area int,house_num_cur smallint,house_num_sum smallint,'\
                         'green_rate float,volum_rate float,construction_rate float,manage_price float,info_add varchar(100),'\
                         'water_price varchar(50),electric_price varchar(50),gas_price varchar(50),'\
                         'network varchar(50),elector varchar(50),security varchar(50),sanitation varchar(50),'\
                         'parking varchar(100),metro varchar(50),bus varchar(50),car varchar(50),'\
                         'kindergarten varchar(50),school varchar(50),university varchar(50),shop_mall varchar(50),'\
                         'hospital varchar(50),post_office varchar(50),bank varchar(50),other_facility varchar(50),'\
                         'property_company varchar(100),building_num_sum smallint)'\
                         'engine=innodb default charset=utf8'
        try:
            cls.cursor.execute(create_command)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Table exist.')
        cls.cnx.commit()

    @classmethod
    def close_connect(cls):
        cls.cursor.close()
        cls.cnx.close()

    @classmethod
    @thread_safe_sql
    def insert_community_info(cls, info_dict):
        # cls.lock.acquire()
        insert_command = 'INSERT INTO community_info'+cls.time_str+'( \
                         code,name,page_url,sell_url,rent_url,record_url,price_cur,ratio_month,address, \
                         community_feature,region,property,manage_type,done_time, \
                         build_company,building_type,building_area,cover_area, \
                         house_num_cur,house_num_sum,green_rate,volum_rate,construction_rate, \
                         manage_price,info_add,water_price,electric_price,gas_price, \
                         network,elector,security,sanitation,parking,metro,bus,car, \
                         kindergarten,school,university,shop_mall,hospital,post_office, \
                         bank,other_facility,property_company,building_num_sum)\
                         VALUES (%(code)s, %(name)s, %(page_url)s, %(sell_url)s, %(rent_url)s, %(record_url)s, %(price_cur)s, %(ratio_month)s,\
                         %(address)s, %(community_feature)s, %(region)s, %(property)s,\
                         %(manage_type)s, %(done_time)s, %(build_company)s,\
                         %(building_type)s, %(building_area)s, %(cover_area)s,\
                         %(house_num_cur)s, %(house_num_sum)s, %(green_rate)s,\
                         %(volum_rate)s, %(construction_rate)s, %(manage_price)s, %(info_add)s, %(water_price)s,\
                         %(electric_price)s, %(gas_price)s, %(network)s, %(elector)s,\
                         %(security)s, %(sanitation)s, %(parking)s, %(metro)s, %(bus)s,\
                         %(car)s, %(kindergarten)s, %(school)s, %(university)s,\
                         %(shop_mall)s, %(hospital)s, %(post_office)s, %(bank)s,\
                         %(other_facility)s, %(property_company)s, %(building_num_sum)s)'
        cls.cursor.execute(insert_command, info_dict)
        cls.cnx.commit()
        # cls.lock.release()

    @classmethod
    @thread_safe_sql
    def select_if_exist(cls, page_url):
        select_command = 'SELECT EXISTS(SELECT 1 FROM community_info'+cls.time_str+' WHERE page_url=%(page_url)s)'
        value = {'page_url': page_url}
        cls.cursor.execute(select_command, value)
        if cls.cursor.fetchall()[0][0] == 1:
            return True
        else:
            return False


