#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install openpyxl
import os.path
import openpyxl

from config import EXCEL_FILE_PATH, TEST_SHEET_NAME
from utils.my_exception.all_exception import *


# 读取excel内容，实现文件驱动自动化执行
def read_excel():
    if not os.path.exists(EXCEL_FILE_PATH):
        raise PathNotExist("路径: %s 不存在" % EXCEL_FILE_PATH)
    excel = openpyxl.load_workbook(EXCEL_FILE_PATH)
    sheet = excel[TEST_SHEET_NAME]
    title = []
    # 创建装载Excel数据的变量
    tuple_list = []
    dict_list = []
    # 逐行循环读取Excel数据
    for value in sheet.values:
        # 判断当前行的第一列的值，是否是数字编号
        if type(value[0]) is int:
            # 将元祖装进List
            tuple_list.append(value)
        else:
            title = value
    # 将数据格式化为字典,即加入标题
    for item in tuple_list:
        # 判断标题数量与数据数量是否一致
        contains_none = list(filter(lambda x: x is None, title))
        if (not contains_none) and title:
            dict_list.append(dict(zip(title, item)))
        else:
            raise ExcelDataColumnNotMatch("标题列数量与数据列数量不匹配, id={}".format(item[1]))
    excel.close()
    return dict_list


if __name__ == '__main__':
    a = read_excel()[1]["预期结果"].split(";")
    print(a)
    b = []
    for i in a:
        if i.startswith("{") or i.startswith("["):
            b.append(eval(i))
        else:
            b.append(i)

    print(b)

