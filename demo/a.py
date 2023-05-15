# from enum import Enum
#
#
# class A(Enum):
#     equals = "="
#     not_equals = "!="
#
#
# import pymysql
# import pymysql
# import time
#
# # 数据库
# db = ""
# cur = ""
# # 现在年月日
# try:
#     # 数据库配置
#     config = {
#         "host": "shop-xo.hctestedu.com",
#         "port": 3306,
#         "user": "api_test",
#         "password": "Aa9999!",
#         "db": 'test_huace1',
#         "charset": "utf8mb4",
#         "cursorclass": pymysql.cursors.DictCursor
#     }
#     db = pymysql.connect(**config)
#     # 游标
#     cur = db.cursor()
# except:
#     print("连接数据库失败")
#     exit(-1)
#
#
# # 查询今天之后的所有天气数据
# def get_day_list():
#     sql_weather_days = "SELECT*FROM author"
#     cur.execute(sql_weather_days)
#     dayList = cur.fetchall()
#     print(dayList)
#     pass
#
# get_day_list()
import jsonpath
#
# print(tuple(["1", "2"]))
# print(jsonpath.jsonpath({"a": "1"}, "$.111"))
# print(1 == 1 == 2)
print(isinstance(["a"], (list, dict)))