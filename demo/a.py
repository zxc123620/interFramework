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
# import jsonpath
#
# print(tuple(["1", "2"]))
# print(jsonpath.jsonpath({"a": "1"}, "$.111"))
# print(1 == 1 == 2)
# print(isinstance(["a"], (list, dict)))
import re

import deepdiff
import pytest


#
#
@pytest.fixture()
def setup_a():
    print("aa执行setup")
    yield 1
    print("aa执行teardown")


@pytest.fixture()
def setup_b():
    print("bb执行setup")
    yield 1
    print("bb执行teardown")


# @pytest.fixture(params=[1, 2])
# def setup_b(request, setup_a):
#     print("测试用例执行之前执行 %s" % request.param)
#     # print(request.param)
#     print(setup_a)
#     yield request.param
#     print("测试用例执行之后执行 %s" % request.param)


# def test_01(setup_b,setup_a):
#     assert 2 == 2

# a = ["a", "b", "c"]
# b = ["b", "c", "d"]
# print(all([i in a for i in b]))

# print([1, 2, 3][4])
# print("sql:1"[len("sql:")])
# result = re.findall("a", "b")
# a = None if not result else result
# print(a)

# print(deepdiff.DeepDiff(1, 1, ignore_string_type_changes=True, ignore_numeric_type_changes=True).pretty())

print(type(eval("1")))
