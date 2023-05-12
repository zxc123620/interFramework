import logging

import allure
import openpyxl
import pytest

from utils.api_keywords.ApiKeyWords import ApiKeyword
from utils.assert_utils.AssertType import AssertType, AssertMethod
from utils.excel_utils.read_excel import read_excel
import utils.log_utils.log_config
from utils.my_exception.all_exception import AssertTypeException

logger = logging.getLogger("main.create_test")
ak = ApiKeyword()
excel_path = r"D:\code\pythonProject\interFrame\excel\api_cases.xlsx"
excel = openpyxl.load_workbook(excel_path)
sheet = excel['Sheet1']
all_val = {}
result = ""


@pytest.mark.parametrize('data', read_excel())
def test_single(data):
    # # 动态生成标题
    # allure.dynamic.title(data[11])
    # 如果存在自定义标题
    logger.info("======================================================")
    logger.info("用例标题: %s" % data['用例名'])
    global result
    if data['用例名'] is not None:
        # 动态生成标题
        allure.dynamic.title(data['用例名'])
    if data['story(小模块)'] is not None:
        # 动态获取story模块名
        allure.dynamic.story(data['story(小模块)'])
    if data['feature(大模块)'] is not None:
        # 动态获取feature模块名
        allure.dynamic.feature(data['feature(大模块)'])
    if data['备注'] is not None:
        # 动态获取备注信息
        allure.dynamic.description('备注')
    if data['级别'] is not None:
        # 动态获取级别信息(blocker、critical、normal、minor、trivial)
        allure.dynamic.severity('级别')
    # 行数
    r = data["编号"] + 1
    # ==============Excel数据解析==============
    try:
        dict_data = {
            'url': data["地址"] + data["路径"],
            'params': eval(data['公共参数(PARAMS)']),
            'headers': eval(data['请求头']),
            data["参数类型"]: eval(data['参数'])  # json/data
        }
    except Exception:
        logger.info("=============实际结果=================")
        logger.info("接口请求格式有误，请检查url、params、headers、data、参数类型")
        sheet.cell(r, 12).value = "请求参数有误，请检查"
        raise
    res = getattr(ak, data['请求方法'])(**dict_data)
    # =================Json提取器=================
    if data['JSON提取_引用名称'] is not None:
        # 遍历分割JSON提取_引用名称
        json_name_str = data['JSON提取_引用名称']
        # 用分号分割varStr字符串，并保存到列表
        json_name_str_list = json_name_str.split(';')
        logger.info("JSON提取_引用名称: %s" % json_name_str_list)
        # 获取列表长度
        length = len(json_name_str_list)
        # 遍历分割JSON表达式
        jsonpath_str = data['JSON表达式']
        jsonpath_str_list = jsonpath_str.split(';')
        logger.info("JSON表达式: %s" % jsonpath_str_list)
        # 循环输出列表值
        for i in range(length):
            # 获取JSON提取_引用名称
            key = json_name_str_list[i]
            # json表达式获取
            json_exp = jsonpath_str_list[i]
            # 字典值获取
            value_json = ak.get_text(res.text, json_exp)
            # 持续添加参数，只要参数名不重复，重复的后面就会覆盖前面的参数
            all_val[key] = value_json
    # 校验类型校验
    assert_types = [i.value for i in AssertType]
    excel_assert_type = data["校验类型"]
    if excel_assert_type in assert_types:
        raise AssertTypeException("校验类型[ %s ]不正确" % data["校验类型"])
    excel_assert_name = AssertType(excel_assert_type).name
    # 结果校验
    result = ak.get_text(res.text, data['校验字段'])
    logger.info("预期结果: %s" % data["预期结果"])
    logger.info("实际结果: %s" % result)
    is_ok, msg = getattr(AssertMethod, excel_assert_name)(data["预期结果"], result)
    sheet.cell(r, 12).value = msg
    assert is_ok, msg
    excel.save(excel_path)

    # 数据库结果校验
    # 如果存在数据库检查并且需要动态关联接口参数
    if data['数据库SQL'] is not None:
        try:
            # 拼接sql
            str_sql = data['数据库SQL']
            # 遍历分割数据库变量
            sql_param_str = data['数据库变量']
            sql_param_list = sql_param_str.split(';')  # ["all_val['VAR_UID']", "all_val['VAR_UNAME']"]
            list1 = []
            # 获取sql参数列表长度
            length = len(sql_param_list)
            # 循环解析all_val[]值并填入list1
            for i in range(length):
                list1.append(eval(sql_param_list[i]))
            sql = str_sql.format(*list1)
            # 实际结果
            sql_check = None
            sql_check = ak.sqlCheck(sql, 1)
            if (sql_check == data[22]):
                sheet.cell(r, 11).value = "通过"
            else:
                sheet.cell(r, 11).value = "不通过"
            excel.save(excel_path)
        except:
            print("=============实际结果=================")
            print("sql有误，请检查")
            sheet.cell(r, 11).value = "sql有误，请检查"
            excel.save(excel_path)
        finally:
            # assert_utils sql_check == data[22]
            pass
    # # 数据库结果校验
    # # 如果存在数据库检查，不需要动态关联接口参数
    # if data[20] is not None:
    #     try:
    #         # 实际结果
    #         sql = None
    #         sql_check = None
    #         sql = data[20]
    #         sql_check = ak.sqlCheck(sql, 1)
    #         if (sql_check == data[22]):
    #             sheet.cell(r, 11).value = "通过"
    #         else:
    #             sheet.cell(r, 11).value = "不通过"
    #         excel.save(excel_path)
    #     except:
    #         print("=============实际结果=================")
    #         print("sql有误，请检查")
    #         sheet.cell(r, 11).value = "sql有误，请检查"
    #         excel.save(excel_path)
    #     finally:
    #         assert_utils sql_check == data[22]
