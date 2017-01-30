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
        select_command = 'SELECT sell_url,rent_url,record_url FROM community_info'
        cls.cursor.execute(select_command)
        return cls.cursor.fetchall()
