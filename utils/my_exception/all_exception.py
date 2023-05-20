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


class AssertNumNotMatchException(ExcelException):
    """
    校验类型、字段、预期结果数量不匹配
    """

    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


class MyMysqlException(Exception):
    """
    mysql异常
    """

    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


class MyMysqlConnException(MyMysqlException):
    """
    mysql异常
    """

    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


class MyMysqlResultNotMatchException(MyMysqlException):
    """
    mysql结果字典与需要用到的变量不匹配异常
    """

    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info
