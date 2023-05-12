#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install openpyxl
import os.path
import openpyxl

from utils.my_exception.all_exception import *

excel_path = r"D:\code\pythonProject\interFrame\excel\api_cases.xlsx"


# 读取excel内容，实现文件驱动自动化执行
def read_excel():
    if not os.path.exists(excel_path):
        raise PathNotExist("路径: %s 不存在" % excel_path)
    excel = openpyxl.load_workbook(excel_path)
    sheet = excel['Sheet1']
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
    print(read_excel())
