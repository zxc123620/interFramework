import logging
import re


from utils.excel_function.excel_function import ExcelFunction
import utils.log_utils.log_config
from config import get_all_value

logger = logging.getLogger("main.dataRegular")


def regular(data: dict):
    """
    进行{{}}替换操作,替换函数和变量
    Args:
        data: 单项数据,需要里面的数据都是字符串
    Returns:
        替换之后的结果,得到字典,返回也是字典
    """
    logger.info("开始正则替换")
    logger.info(data)
    temp = re.sub("{{func:(.*?)\((.*?)\)}}", __format_method, str(data))  # 进行函数替换操作
    result = re.sub("{{(.*?)}}", __format_val, temp)  # 进行变量替换操作‘
    result = eval(result)
    logger.info("正则替换后的data: %s" % result)
    return result


def __format_val(temp):
    """
    格式化变量 {{}}
    Args:
        temp: 得到的正则结果 其中变量的key
    Returns:
        字符串结果
    """

    value = temp.group(1)
    logger.debug("需要格式化的变量: %s" % value)
    if "[" in value:
        logger.debug("变量不为字符串")
        new_value = value[:value.index("[")]
        logger.debug(new_value)
        inner_value = value[value.index("[") + 1:value.index("]")]
        if re.search("(\d+)", inner_value):
            logger.debug("变量方括号中的值为数字")
            logger.info(get_all_value())
            result = get_all_value().get(new_value, 'None')[int(inner_value)]
            logger.debug("变量获取,得到结果: %s" % result)
            return str(result)
        elif re.search("([a-z,A-Z]+)", inner_value):
            logger.debug("变量方括号中的值为字符串")
            result = get_all_value().get(new_value, 'None')[inner_value]
            logger.debug("变量获取,得到结果: %s" % result)
            return str(result)
    else:
        logger.debug("变量为字符串")
        result = get_all_value().get(value, 'None')
        logger.debug("变量获取,得到结果: %s" % result)
        return str(result)


def __format_method(temp):
    """
    格式化函数 {{func:xxx}} 将得到的函数与参数进行调用,并将结果进行返回
    Args:
        temp: 得到的正则结果 其中有函数名和函数参数
    Returns:
        调用结果
    """
    func_name, func_args = temp.group(1), temp.group(2)
    func_args_list = func_args.split(",")  # 多个参数
    logger.debug("需要格式化的函数: %s , 参数%s" % (func_name, func_args_list))
    result = str(getattr(ExcelFunction, func_name)(*func_args_list))
    logger.debug("函数调用完成,得到结果: %s" % result)
    return result


if __name__ == '__main__':
    a = {'编号': 3, 'id': 'cart.del.1', 'feature(大模块)': '华测电商', 'story(小模块)': '删除购物车', '用例名': '能删除当前用户对应的购物车数据（多个）',
         '前置操作': 'request:1;request:2;request:3', '后置操作': None, '地址': 'http://shop-xo.hctestedu.com/index.php?s=',
         '路径': 'api/cart/delete&application=app&application_client_type=weixin&token={{token}}', '请求方法': 'post',
         '公共参数(PARAMS)': 'None', '请求头': '{"Content-Type": "application/json"}', '参数': '{"id":\'{{a[1]}}\'}',
         '参数类型': 'data', '文件': None, '校验字段': '$.msg', '校验类型': 'eq', '预期结果': '删除成功', '检查结果': None, 'JSON提取_引用名称': None,
         'JSON表达式': None, '正则提取_引用名称': None, '正则表达式': None, '备注': '能删除当前用户对应的购物车数据（多个）', '级别': 'blocker',
         '数据库SQL引用': None, '引用数据库变量': None, '数据库预期': None}
    print(regular(a))
    # # print(re.findall("{{(.*?)}}", str(a)))
    # print(re.search("([a-z,A-Z]+)", "123"))
    # print(re.search("(\d+)", "123").group(1))
    # value = "aaa[1]"
    # print(value[list(value).index("[")+1:list(value).index("]")])
