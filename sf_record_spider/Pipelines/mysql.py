import mysql.connector
from mysql.connector import errorcode
from sf_record_spider import settings
import time
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

    @classmethod
    def create_tables(cls):
        create_command = []
        create_command.append('CREATE TABLE sell_info'+cls.time_str+'(sell_info_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,'\
                            'code varchar(50),release_time date, price_all int,price_per int,first_pay int,'\
                            'month_pay int,floor varchar(50),area_build int,direction varchar(50),'\
                            'decoration varchar(50),house_model varchar(50),build_time int,'\
                            'house_structure varchar(50),house_type varchar(50),'\
                            'property_type varchar(50),page_url varchar(255),last_deal_time date,'\
                            'building_type varchar(100),crawl_time date)engine=innodb default charset=utf8')
        create_command.append('CREATE TABLE relation_community_sell'+cls.time_str+'(sell_info_id int NOT NULL,'\
                            'community_info_id int,foreign key(sell_info_id) references sell_info'+cls.time_str+'(sell_info_id) '\
                            'on delete cascade on update cascade)engine=innodb default charset=utf8')
        create_command.append('CREATE TABLE rent_info'+cls.time_str+'(rent_info_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,'\
                            'code varchar(50),update_time date,price int,rate float,pay_type varchar(50),'\
                            'house_type varchar(50),house_model varchar(50),area_build int,floor varchar(50),'\
                            'direction varchar(50),decoration varchar(50),support_bed BOOLEAN,'\
                            'support_furniture BOOLEAN,support_gas BOOLEAN,support_warm BOOLEAN,'\
                            'support_network BOOLEAN,support_tv BOOLEAN,support_condition BOOLEAN,'\
                            'support_fridge BOOLEAN,support_wash BOOLEAN,support_water BOOLEAN,'\
                            'page_url varchar(255),rent_type varchar(50),crawl_time date)'\
                            'engine=innodb default charset=utf8')
        create_command.append('CREATE TABLE relation_community_rent'+cls.time_str+'(rent_info_id int NOT NULL,'\
                            'community_info_id int,foreign key(rent_info_id) references rent_info'+cls.time_str+'(rent_info_id) '\
                            'on delete cascade on update cascade)engine=innodb default charset=utf8')
        create_command.append('CREATE TABLE record_sell_info'+cls.time_str+'(record_sell_info_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,'\
                            'house_model varchar(50),floor varchar(50),direction varchar(50),area_build int,'\
                            'sell_time date,price_all int,price_per int)engine=innodb default charset=utf8')
        create_command.append('CREATE TABLE relation_community_record_sell'+cls.time_str+'(record_sell_info_id int NOT NULL,'\
                            'community_info_id int,foreign key(record_sell_info_id) '\
                            'references record_sell_info'+cls.time_str+'(record_sell_info_id) on delete cascade on update cascade)'\
                            'engine=innodb default charset=utf8')
        create_command.append('CREATE TABLE record_rent_info'+cls.time_str+'(record_rent_info_id'\
                            ' int NOT NULL PRIMARY KEY AUTO_INCREMENT,house_model varchar(50),'\
                            'floor varchar(50),direction varchar(50),area_build int,sell_time date,price int)'\
                            'engine=innodb default charset=utf8')
        create_command.append('CREATE TABLE relation_community_record_rent'+cls.time_str+'(record_rent_info_id'\
                            ' int NOT NULL,community_info_id int,foreign key(record_rent_info_id)'\
                            ' references record_rent_info'+cls.time_str+'(record_rent_info_id) on delete cascade on update cascade)'\
                            'engine=innodb default charset=utf8')
        for sql_command in create_command:
            try:
                cls.cursor.execute(sql_command)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('Table exist.')
            finally:
                cls.cnx.commit()

    @classmethod
    def close_connect(cls):
        cls.cursor.close()
        cls.cnx.close()

    @classmethod
    def select_community_url(cls):
        select_command = 'SELECT sell_url,rent_url,record_url,community_info_id FROM community_info'+cls.time_str
        cls.cursor.execute(select_command)
        return cls.cursor.fetchall()
        # return [('http://jinyutixiangwk025.fang.com/chushou/'
        #          , 'http://jinyutixiangwk025.fang.com/chuzu/'
        #          , 'http://jinyutixiangwk025.fang.com/chengjiao/'
        #          , 4588)]

    @classmethod
    def insert_sell_info(cls, insert_dict, community_info_id):
        insert_command = 'INSERT INTO sell_info'+cls.time_str+'(code,release_time,price_all,'\
                         'price_per,first_pay,month_pay,floor,area_build,direction,'\
                         'decoration,house_model,build_time,house_structure,house_type,property_type,'\
                         'page_url,last_deal_time,building_type,crawl_time)'\
                         'VALUES(%(code)s,%(release_time)s,%(price_all)s,%(price_per)s,%(first_pay)s,'\
                         '%(month_pay)s,%(floor)s,%(area_build)s,%(direction)s,%(decoration)s,%(house_model)s,'\
                         '%(build_time)s,%(house_structure)s,%(house_type)s,%(property_type)s,%(page_url)s,'\
                         '%(last_deal_time)s,%(building_type)s,%(crawl_time)s)'
        relation_command = 'INSERT INTO relation_community_sell'+cls.time_str+'(sell_info_id,community_info_id)'\
                           'VALUES(%(sell_info_id)s,%(community_info_id)s)'
        relation_dict = {}
        relation_dict['community_info_id'] = community_info_id
        cls.cursor.execute(insert_command, insert_dict)
        relation_dict['sell_info_id'] = cls.cursor.lastrowid
        cls.cursor.execute(relation_command, relation_dict)
        cls.cnx.commit()

    @classmethod
    def insert_rent_info(cls, insert_dict, community_info_id):
        insert_command = 'INSERT INTO rent_info'+cls.time_str+'(code,update_time,price,'\
                         'rate,pay_type,house_type,house_model,area_build,floor,'\
                         'direction,decoration,support_bed,support_furniture,'\
                         'support_gas,support_warm,support_network,support_tv,'\
                         'support_condition,support_fridge,support_wash,support_water,'\
                         'page_url,rent_type,crawl_time)'\
                         'VALUES(%(code)s,%(update_time)s,%(price)s,'\
                         '%(rate)s,%(pay_type)s,%(house_type)s,%(house_model)s,%(area_build)s,%(floor)s,'\
                         '%(direction)s,%(decoration)s,%(support_bed)s,%(support_furniture)s,'\
                         '%(support_gas)s,%(support_warm)s,%(support_network)s,%(support_tv)s,'\
                         '%(support_condition)s,%(support_fridge)s,%(support_wash)s,%(support_water)s,'\
                         '%(page_url)s,%(rent_type)s,%(crawl_time)s)'
        relation_command = 'INSERT INTO relation_community_rent'+cls.time_str+'(rent_info_id,community_info_id)'\
                           'VALUES(%(rent_info_id)s,%(community_info_id)s)'
        relation_dict = {}
        relation_dict['community_info_id'] = community_info_id
        cls.cursor.execute(insert_command, insert_dict)
        relation_dict['rent_info_id'] = cls.cursor.lastrowid
        cls.cursor.execute(relation_command, relation_dict)
        cls.cnx.commit()

    @classmethod
    def insert_record_sell_info(cls, insert_dict, community_info_id):
        insert_command = 'INSERT INTO record_sell_info'+cls.time_str+'(house_model,floor,direction,'\
                         'area_build,sell_time,price_all,price_per)'\
                         'VALUES(%(house_model)s,%(floor)s,%(direction)s,%(area_build)s,'\
                         '%(sell_time)s,%(price_all)s,%(price_per)s)'
        relation_command = 'INSERT INTO relation_community_record_sell'+cls.time_str+'(record_sell_info_id,community_info_id)'\
                           'VALUES(%(record_sell_info_id)s,%(community_info_id)s)'
        relation_dict = {}
        relation_dict['community_info_id'] = community_info_id
        cls.cursor.execute(insert_command, insert_dict)
        relation_dict['record_sell_info_id'] = cls.cursor.lastrowid
        cls.cursor.execute(relation_command, relation_dict)
        cls.cnx.commit()

    @classmethod
    def insert_record_rent_info(cls, insert_dict, community_info_id):
        insert_command = 'INSERT INTO record_rent_info'+cls.time_str+'(house_model,floor,direction,'\
                         'area_build,sell_time,price)'\
                         'VALUES(%(house_model)s,%(floor)s,%(direction)s,%(area_build)s,'\
                         '%(sell_time)s,%(price)s)'
        relation_command = 'INSERT INTO relation_community_record_rent'+cls.time_str+'(record_rent_info_id,community_info_id)'\
                           'VALUES(%(record_rent_info_id)s,%(community_info_id)s)'
        relation_dict = {}
        relation_dict['community_info_id'] = community_info_id
        cls.cursor.execute(insert_command, insert_dict)
        relation_dict['record_rent_info_id'] = cls.cursor.lastrowid
        cls.cursor.execute(relation_command, relation_dict)
        cls.cnx.commit()