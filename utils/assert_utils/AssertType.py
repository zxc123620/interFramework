from enum import Enum


class AssertType(Enum):
    """
    定义断言枚举类
    """
    equals = "eq"
    not_equals = "neq"
    str_contains = "str_in"
    dict_contains = "dict_in"


class AssertMethod:
    @staticmethod
    def equals(expect_value, actual_value):
        """
        相等性质判断
        :param expect_value: 预期结果
        :param actual_value: 实际结果
        :return:
        """
        if expect_value == actual_value:
            return True, "通过"
        return False, "预期结果与实际结果不一致"

    @staticmethod
    def not_equals(expect_value, actual_value):
        """
        不等性质判断
        :param expect_value: 预期结果
        :param actual_value: 实际结果
        :return:
        """
        assert expect_value != actual_value, "预期结果与实际结果不一致"

    @staticmethod
    def str_contains(expect_value, actual_value):
        """
        字符串包含判断
        :param expect_value: 预期结果
        :param actual_value: 实际结果
        :return:
        """
        assert expect_value in actual_value, "预期结果不包含在实际结果中"

    @staticmethod
    def dict_contains(expect_value: dict, actual_value: dict):
        """
        字典包含判断
        :param expect_value: 预期结果
        :param actual_value: 实际结果
        :return:
        """
        actual_keys = actual_value.keys()
        for expect_key, value in expect_value.items():
            assert expect_key in actual_keys, "预期结果中的字典项在实际结果中不存在"
            assert value in actual_value[expect_key], "预期结果中的值在实际结果中不存在"


if __name__ == '__main__':
    getattr(AssertMethod, "equals")(1, 2)
