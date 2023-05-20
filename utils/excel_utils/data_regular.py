import logging
import re

from config import ALL_VALUE
from utils.excel_function.excel_function import ExcelFunction
import utils.log_utils.log_config

logger = logging.getLogger("main.dataRegular")


def regular(data: dict):
    """
    进行{{}}替换操作,替换函数和变量
    Args:
        data: 单项数据,需要里面的数据都是字符串
    Returns:
        替换之后的结果,得到字典,返回也是字典
    """
    temp = re.sub("{{func:(.*?)\((.*?)\)}}", __format_method, str(data))  # 进行函数替换操作
    result = re.sub("{{(.*?)}}", __format_val, temp)  # 进行变量替换操作
    return eval(result)


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
    result = ALL_VALUE.get(value, 'None')
    logger.debug("变量获取,得到结果: %s" % result)
    return result


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


# if __name__ == '__main__':
#     for i in read_excel():
#         print(i)
#         print(regular(i))
