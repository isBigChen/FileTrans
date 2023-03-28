import pymysql
from Logger import logger

SERVER_IP = "192.168.218.129"
SERVER_PORT = 3306
USER = "root"
PASSWORD = "123456"
DATABASE = "file_trans"


class MysqlHandler:
    def __init__(self):
        self.server_ip = SERVER_IP
        self.server_port = SERVER_PORT
        self.user = USER
        self.password = PASSWORD
        self.database = DATABASE
        try:
            self.db = pymysql.connect(host=self.server_ip, port=self.server_port, user=self.user,
                                      passwd=self.password, db=self.database, charset='utf8')
            self.cursor = self.db.cursor()
        except Exception as e:
            logger.debug(e)

    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
        except Exception as e:
            logger.debug(e)

    def query_handler(self, query_sql):
        try:
            self.cursor.execute(query_sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            logger.debug(e)

    def operate_handler(self, operate_sql):
        try:
            self.cursor.execute(operate_sql)
            self.db.commit()
        except Exception as e:
            logger.debug(e)



