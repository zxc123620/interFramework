import json
import logging

import allure
import jsonpath
import requests

from utils.log_utils.log_decorate import log_decorator

logger = logging.getLogger("main.apiKeyword")


class ApiKeyword:

    @staticmethod
    @allure.step("发送get请求")
    @log_decorator(True)
    def get(url, params=None, **kwargs):
        res = requests.get(url, params=params, **kwargs)

    @staticmethod
    @allure.step("发送post请求")
    @log_decorator(True)
    def post(url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, **kwargs)

    @staticmethod
    @allure.step("获取结果")
    def get_text(res, json_path):
        return jsonpath.jsonpath(json.loads(res), json_path)[0]
