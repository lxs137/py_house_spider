import mysql.connector
from mysql.connector import errorcode
from sf_record_spider import settings
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
    def select_community_url(cls):
        # select_command = 'SELECT sell_url,rent_url,record_url,community_info_id FROM community_info'
        # cls.cursor.execute(select_command)
        # return cls.cursor.fetchall()
        return [('http://jinyutixiangwk025.fang.com/chushou/'
                 , 'http://jinyutixiangwk025.fang.com/chuzu/'
                 , 'http://jinyutixiangwk025.fang.com/chengjiao/'
                 , 4588)]

    @classmethod
    def insert_sell_info(cls, insert_dict, community_info_id):
        insert_command = 'INSERT INTO sell_info(code,release_time,price_all,'\
                         'price_per,first_pay,month_pay,floor,area_build,direction,'\
                         'decoration,house_model,build_time,house_structure,house_type,property_type)'\
                         'VALUES(%(code)s,%(release_time)s,%(price_all)s,%(price_per)s,%(first_pay)s,'\
                         '%(month_pay)s,%(floor)s,%(area_build)s,%(direction)s,%(decoration)s,%(house_model)s,'\
                         '%(build_time)s,%(house_structure)s,%(house_type)s,%(property_type)s)'
        relation_command = 'INSERT INTO relation_community_sell(sell_info_id,community_info_id)'\
                           'VALUES(%(sell_info_id)s,%(community_info_id)s)'
        relation_dict = {}
        relation_dict['community_info_id'] = community_info_id
        cls.cursor.execute(insert_command, insert_dict)
        relation_dict['sell_info_id'] = cls.cursor.lastrowid
        cls.cursor.execute(relation_command, relation_dict)
        cls.cnx.commit()