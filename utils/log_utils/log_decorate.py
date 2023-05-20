import logging
from functools import wraps

logger = logging.getLogger("main.requestLog")


def log_decorator(switch: bool):
    """
    封装日志装饰器, 打印请求信息
    :param switch: 定义日志开关
    :return:
    """

    def decorator(func):
        @wraps(func)
        def swapper(*args, **kwargs):
            # 判断日志为开启状态，才打印日志
            res = func(*args, **kwargs)
            # 判断日志开关为开启状态
            if switch and kwargs.get("files", None) is None:
                _log_msg = f"\n请求路径: {res.request.url}\n" \
                           f"请求方式: {res.request.method}\n" \
                           f"请求头: {res.request.headers}\n" \
                           f"请求体: {res.request.body}\n" \
                           f"响应内容: {res.text}\n" \
                           f"响应状态码: {res.status_code}"
            else:
                _log_msg = f"\n请求路径: {res.request.url}\n" \
                           f"请求方式: {res.request.method}\n" \
                           f"请求头: {res.request.headers}\n" \
                           f"响应状态码: {res.status_code}"
                # f"响应内容: {res.text}\n" \
            if res.status_code == 200:
                logger.info(_log_msg)
            else:
                logger.error(_log_msg)
            return res

        return swapper

    return decorator
