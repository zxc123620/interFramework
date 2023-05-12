class ExcelException(Exception):
    """
    excel相关异常
    """

    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


class PathNotExist(ExcelException):
    """
    路径不存在异常
    """

    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


class ExcelDataColumnNotMatch(ExcelException):
    """
    标题缺失或者列表缺失异常
    """

    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


class AssertTypeException(ExcelException):
    """
    校验类型不正确
    """

    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info
