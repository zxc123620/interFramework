import logging

from dbutils.pooled_db import PooledDB
import pymysql.cursors

from utils.my_exception.all_exception import MyMysqlConnException
import utils.log_utils.log_config
logger = logging.getLogger("main.mysql")


class MysqlPool:
    config = {
        'creator': pymysql,
        'host': "shop-xo.hctestedu.com",
        'port': 3306,
        'user': "api_test",
        'password': "Aa9999!",
        'db': "shopxo_hctested",
        'charset': "utf8",
        'maxconnections': 10,  # 连接池最大连接数量
        'cursorclass': pymysql.cursors.DictCursor
    }
    pool = PooledDB(**config)

    def __enter__(self):
        try:
            self.conn = MysqlPool.pool.connection()
            self.cursor = self.conn.cursor()
            return self
        except Exception:
            logger.error("数据库连接异常,参数为: %s" % MysqlPool.config)
            raise MyMysqlConnException("数据库连接异常")

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    """
            host='shop-xo.hctestedu.com',
            port=3306,
            user='api_test',
            passwd='Aa9999!',
            database='shopxo_hctested',
            charset='utf8')
    """
    with MysqlPool() as db:
        db.cursor.execute("select id from sxo_goods")
        print(list(db.cursor.fetchone().values()))
