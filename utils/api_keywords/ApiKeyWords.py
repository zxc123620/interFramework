import json
import logging
import os

import allure
import jsonpath
import requests

from config import ROOT_PATH, EXCEL_FILE_PATH
from utils.log_utils.log_decorate import log_decorator
from utils.my_exception.all_exception import PathNotExist

logger = logging.getLogger("main.apiKeyword")


class ApiKeyword:
    """
    1、发送请求(目前只支持get、post）、获取响应结果
    2、json提取
    """
    @staticmethod
    @allure.step("发送get请求")
    @log_decorator(True)
    def get(url, params=None, **kwargs):
        """
        发送get请求
        Args:
            url: 请求路径
            params:  请求参数
            **kwargs:  其他参数

        Returns:
            响应结果

        """
        res = requests.get(url, params=params, verify=False, **kwargs)
        # if res.status_code == requests.codes.ok:
        return res

    @staticmethod
    @allure.step("发送post请求")
    @log_decorator(True)
    def post(url, data=None, json=None, **kwargs):
        """
        发送post请求
        Args:
            url: 请求路径
            data: 请求data
            json:  请求json
            **kwargs:  其他参数 files ...

        Returns:

        """
        return requests.post(url, data=data, json=json, verify=False, **kwargs)

    @staticmethod
    @allure.step("json提取")
    def get_text(res, json_path, multiple=False):
        """
        json提取
        Args:
            res: 待提取的内容(str)
            json_path: json_path语法
            multiple: 是否提取单个,默认为FALSE,返回第一个值,如果为true,则返回多个值
        Returns:
            返回FALSE表示没找到,返回str表示multiple=False时返回第一个匹配到的值,返回list表示multiple=True时返回所有匹配到的结果
        """
        res = jsonpath.jsonpath(json.loads(res), json_path)
        if res:
            return res if multiple else res[0]
        return res
