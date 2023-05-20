import datetime
import decimal
import logging
import re
import allure
import openpyxl
import pytest
import os
import requests

from config import ROOT_PATH, ALL_VALUE, DATA_SET_NAME
from utils.api_keywords.ApiKeyWords import ApiKeyword
from utils.assert_utils.AssertType import AssertType, AssertMethod
from utils.excel_utils.read_excel import read_excel, regular_excel_data
import utils.log_utils.log_config  # 不能删除
from utils.my_exception.all_exception import AssertTypeException, AssertNumNotMatchException, PathNotExist, \
    MyMysqlResultNotMatchException
from config import EXCEL_FILE_PATH, TEST_SHEET_NAME, SQL_SHEET_NAME
from utils.mysql_utils.mysql_util import MysqlPool

logger = logging.getLogger("main.testcase")
excel = openpyxl.load_workbook(EXCEL_FILE_PATH)
case_sheet = excel[TEST_SHEET_NAME]
sql_sheet = excel[SQL_SHEET_NAME]
data_set_sheet = excel[DATA_SET_NAME]
sql_raw_data = read_excel(SQL_SHEET_NAME)
data_set_raw_data = read_excel(DATA_SET_NAME)


@pytest.fixture(params=read_excel(TEST_SHEET_NAME))
def set_allure_name(request):
    """
    开始执行用例,进行命名
    Args:
        request:
    Returns:

    """
    logger.info("======================================================")
    logger.info("用例标题: %s" % request.param['用例名'])
    logger.info("数据: %s" % request.param)
    # if request.param['用例名'] is not None:
    #     # 动态生成标题
    #     allure.dynamic.title(request.param['用例名'])
    if request.param['story(小模块)'] is not None:
        # 动态获取story模块名
        allure.dynamic.story(request.param['story(小模块)'])
    if request.param['feature(大模块)'] is not None:
        # 动态获取feature模块名
        allure.dynamic.feature(request.param['feature(大模块)'])
    # if request.param['备注'] is not None:
    #     # 动态获取备注信息
    #     allure.dynamic.description(request.param['备注'])
    if request.param['级别'] is not None:
        # 动态获取级别信息(blocker、critical、normal、minor、trivial)
        allure.dynamic.severity('级别')
    return regular_excel_data(request.param)


@pytest.fixture()
def case_pre_function(set_allure_name):
    """
    前后置操作
    Args:
        set_allure_name:
    Returns:

    """
    data = set_allure_name
    # ==============执行用例前进行的操作==============
    logger.info("============进行前置操作===========")
    setup_teardown_func(data, "前置操作")
    yield data
    logger.info("============进行后置操作===========")
    setup_teardown_func(data, "后置操作")


@pytest.fixture()
def send(case_pre_function):
    """
    发起请求
    Args:
        case_pre_function:

    Returns:

    """
    logger.info("============发送请求============")
    data = case_pre_function
    return data, send_request(data)


@pytest.fixture()
def json_extract(send):
    """
    JSON提取
    Args:
        send:

    Returns:

    """
    data, res = send
    json_extraction(data, res)


@pytest.fixture()
def regular_extract(send):
    """
    正则提取
    Args:
        send:

    Returns:

    """
    data, res = send
    regular_extraction(data, res)


def setup_teardown_func(data, name):
    """
    前后置操作
    Args:
        data: excel单行数据
        name: 前置操作 或者 后置操作

    Returns:

    """
    if data[name] is not None:
        setup_step_list = data[name].replace(" ", "").replace("\n", "").split(";")
        for setup_step in setup_step_list:
            try:
                logger.info("进行%s[%s]" % (name, setup_step))
                if str(setup_step).startswith("request:"):
                    setup_step = setup_step[len("request:"):]
                    data_set_data = regular_excel_data(data_set_raw_data[eval(setup_step) - 1])  # 进行正则替换操作
                    res = send_request(data_set_data)  # 在 “数据集”中获取数据并发送请求
                    json_extraction(data_set_data, res)  # JSON提取
                    regular_extraction(data_set_data, res)  # 正则提取
                elif str(setup_step).startswith("sql:"):
                    sql_request(int(str(setup_step)[len("sql:"):]))  # sql请求保存变量到全局
            except Exception:
                logger.error("进行前置操作时操作,请检查前置操作中各类id是否正确")
                raise


def send_request(data):
    """
    发起请求
    Args:
        data: excel中的单行数据
    Returns:

    """
    # ==============解析文件==============
    with allure.step("发起http请求:"):
        logger.info("=======发起http请求=======")
        r = str(data["编号"] + 1)
        file_str = data["文件"]
        if file_str is None:
            files = None
        else:
            file_list = []
            file_dict = eval(file_str)
            for key, value in file_dict.items():
                value = ROOT_PATH + "/upload_files/" + value
                if not os.path.exists(value):
                    raise PathNotExist("路径不存在: %s" % value)
                file_list.append((key, (key, open(value, "rb"))))  # ('1.png', ('1.png', open('logo.png', 'rb')))
            files = tuple(file_list)
        # ==============解析Excel数据==============
        try:
            url = data["地址"] + data["路径"] if data["路径"] is not None else data["地址"]
            dict_data = {
                'url': url,
                'params': eval(data['公共参数(PARAMS)']),
                'headers': eval(data['请求头']),
                data["参数类型"]: eval(data['参数']),  # json/data
                "files": files
            }
        except Exception:
            logger.error("接口请求格式有误，请检查url、params、headers、data、参数类型、文件")
            case_sheet["S" + r] = "请求参数有误，请检查"
            raise
        # ==============发起请求==============
        res = getattr(ApiKeyword, data['请求方法'])(**dict_data)  # 发起请求
        if res.status_code != requests.codes.ok:  # 初步判断 200才能往下走
            case_sheet["S" + r] = "响应码不为200"
            excel.save(EXCEL_FILE_PATH)
            assert False, "相应码不为200"
        else:
            return res


def json_extraction(data, res):
    """
    json提取
    Args:
        data: excel单行数据
        res: 请求的返回值
    Returns:

    """
    with allure.step("json提取"):
        logger.info("=======json提取=======")
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
                value_json = ApiKeyword.get_text(res.text, json_exp)
                # 持续添加参数，只要参数名不重复，重复的后面就会覆盖前面的参数
                ALL_VALUE[key] = value_json


def regular_extraction(data, res):
    """
    正则提取
    Args:
        data: excel单行数据
        res: 请求的返回值
    Returns:

    """
    with allure.step("正则提取_引用名称"):
        logger.info("=======正则提取=======")
        if data['正则提取_引用名称'] is not None:
            # 遍历分割 正则提取_引用名称
            regular_name_str = data['正则提取_引用名称']
            # 用分号分割varStr字符串，并保存到列表
            regular_name_str_list = regular_name_str.split(';')
            logger.info("正则提取_引用名称: %s" % regular_name_str_list)
            # 获取列表长度
            length = len(regular_name_str_list)
            # 遍历分割正则表达式
            regular_str = data['正则表达式']
            regular_str_list = regular_str.split(';')
            logger.info("正则表达式: %s" % regular_str_list)
            # 循环输出列表值
            for i in range(length):
                # 获取提取_引用名称
                key = regular_name_str_list[i]
                # 正则表达式获取
                regular_exp = regular_str_list[i]
                # 字典值获取
                value_regular = re.findall(regular_exp, res.text)
                # 持续添加参数，只要参数名不重复，重复的后面就会覆盖前面的参数
                ALL_VALUE[key] = None if not value_regular else value_regular


def sql_request(sql_id):
    """
    sql请求
    Args:
        sql_id: excel -> jdbc_request -> 编号

    Returns:

    """
    with allure.step("发送SQL请求"):
        logger.info("=======发送SQL请求=======")
        sql_item = sql_raw_data[sql_id - 1]  # 根据引用id查找sql语句对应的列
        logger.info("对应的jdbc_request请求id为: %s" % sql_item["id"])
        logger.info("sql语句替换前: %s" % sql_item["数据库语句"])
        sql_item = regular_excel_data(sql_item)  # 对sql语句对应的列进行正则替换
        logger.info("sql语句替换后: %s" % sql_item["数据库语句"])
        temp = {}
        with MysqlPool() as db:
            db.cursor.execute(sql_item["数据库语句"])
            sql_result_dict = db.cursor.fetchone()  # none 或者 字典
        logger.info("SQL语句执行结果: %s" % sql_result_dict)
        # 检查 数据库引用变量 与 SQL执行结果 是否为空
        if sql_item["数据库引用变量"] is not None and sql_result_dict is not None:
            sql_var_list = str(sql_item["数据库引用变量"]).replace(" ", "").split(";")
            sql_result_keys = list(sql_result_dict.keys())
            logger.info("引用变量: %s, SQL执行结果变量: %s" % (sql_var_list, sql_result_keys))
            # 检查 数据库引用变量在SQL语句执行结果中是否都存在
            if not all([sql_var in sql_result_keys for sql_var in sql_var_list]):  # 数据库引用变量在SQL语句执行结果中有些变量不存在
                logger.info("数据库引用变量在SQL语句执行结果中不存在")
                raise MyMysqlResultNotMatchException("数据库引用变量在SQL语句执行结果中不存在")
            # 数据库引用变量在SQL语句执行结果中都存在
            temp.update(
                dict(
                    zip(
                        tuple(sql_var_list),
                        tuple([sql_result_dict[sql_var] for sql_var in sql_var_list])
                    )
                )
            )
        ALL_VALUE.update(temp)  # 更新到全局变量


@pytest.fixture()
def assert_result_check(send):
    """
    断言检查
    Args:
    Returns:
    """
    data, res = send
    r = str(data["编号"] + 1)
    # =================校验类型校验=================
    # 校验类型校验
    logger.info("============查看用例的结果是否有误============")
    assert_types = [i.value for i in AssertType]
    excel_assert_types = str(data["校验类型"]).split(";")  # 校验类型(多个)
    excel_json_assert_fields = data['校验字段'].split(";")  # 校验字段(多个)
    excel_expected_values = data['预期结果'].split(";")  # 预期结果(多个)
    if not all([i in assert_types for i in excel_assert_types]):  # 如果校验类型中有不符合的字符
        error_info = "校验类型[ %s ]不正确,可用校验参数: %s " % (excel_assert_types, assert_types)
        logger.error(error_info)  # 日志打印
        case_sheet["S" + r] = error_info  # 保存结果到excel
        excel.save(EXCEL_FILE_PATH)  # 保存操作
        raise AssertTypeException(error_info)
    if not (len(excel_assert_types) == len(excel_json_assert_fields) == len(excel_expected_values)):  # 查看数量是否一致
        info = "校验类型、字段、预期结果数量不匹配: %s %s %s" % (len(excel_assert_types), len(excel_json_assert_fields), len(
            excel_expected_values))
        logger.error(info)  # 日志打印
        case_sheet["S" + r] = info
        excel.save(EXCEL_FILE_PATH)
        raise AssertNumNotMatchException(info)
    # =================预期结果进行转换操作=================
    # 预期结果进行转换操作
    temp_list = []
    for i in excel_expected_values:
        # if i.startswith("{") or i.startswith("[") or i == "None":
        #     temp_list.append(eval(i))
        # else:
        #     temp_list.append(i)
        temp_list.append(eval(i))
    excel_expected_values = temp_list
    return excel_assert_types, excel_json_assert_fields, excel_expected_values


def test_case(json_extract, regular_extract, send, assert_result_check):
    logger.info("============结果检查============")
    excel_assert_types, excel_json_assert_fields, excel_expected_values = assert_result_check
    data, res = send
    r = str(data["编号"] + 1)
    if data['备注'] is not None:
        # 动态获取备注信息
        allure.dynamic.description(data['备注'])
    if data['用例名'] is not None:
        # 动态生成标题
        allure.dynamic.title(data['用例名'])
    # 数量相等的情况
    # =================预期结果校验=================
    for i in range(len(excel_assert_types)):  # 校验参数类型
        excel_assert_type = excel_assert_types[i]  # 校验类型(单个)
        excel_json_assert_field = excel_json_assert_fields[i]  # json校验字段(单个)
        excel_expected_value = excel_expected_values[i]  # 预期结果(单个)
        excel_assert_name = AssertType(excel_assert_type).name
        # 结果校验
        logger.info("=====进行校验 %s" % i)
        result_a = ApiKeyword.get_text(res.text, excel_json_assert_field,
                                       multiple=isinstance(excel_expected_value, (list, dict)))
        logger.info("预期结果: %s, 类型: %s" % (excel_expected_value, type(excel_expected_value)))
        logger.info("实际结果(false表示没找到): %s,类型: %s" % (result_a, type(result_a)))
        is_ok, msg = getattr(AssertMethod, excel_assert_name)(excel_expected_value, result_a)
        case_sheet["S" + r] = msg
        logger.info("将结果: %s %s 输入到表格 %s 中" % (is_ok, msg, "N" + r))
        excel.save(EXCEL_FILE_PATH)
        assert is_ok, msg
    # 数据库校验
    if data['数据库SQL引用'] is not None and sql_raw_data:
        try:
            logger.info("=====进行SQL结果校验")
            sql_request(int(data['数据库SQL引用']))
            # 引用数据库变量
            sql_vars_list = data["引用数据库变量"].split(";")
            sql_expected_list = data["数据库预期"].split(";")
            logger.info("数据库预期: %s" % sql_expected_list)
            for i in range(len(sql_vars_list)):
                sql_expected = eval(sql_expected_list[i])
                # if sql_expected.startswith("{") or sql_expected.startswith("[") or sql_expected == "None":
                #     sql_expected = eval(sql_expected)
                val_raw = ALL_VALUE.get(sql_vars_list[i], None)
                if val_raw is not None and isinstance(val_raw, (int, decimal.Decimal, datetime.datetime)):
                    val_raw = str(val_raw)
                if val_raw == sql_expected:
                    case_sheet["S" + r] = "通过"
                    excel.save(EXCEL_FILE_PATH)
                else:
                    error_info = "不通过,数据库校验失败,预期: %s,实际: %s" % (
                        sql_expected, ALL_VALUE.get(sql_vars_list[i], None))
                    case_sheet["S" + r] = error_info
                    logger.error(error_info)
                    excel.save(EXCEL_FILE_PATH)
                    assert False, error_info
        except IndexError:
            info = "%s 在jdbc_request中不存在" % int(data['数据库SQL引用'])
            logger.error(info)
            raise IndexError(info)
        except AssertionError:
            raise
        except Exception:
            logger.error("sql有误，请检查")
            raise
    else:
        logger.info("数据引用为空或者jdbc_request为空,不进行SQL断言判断")
    pass
