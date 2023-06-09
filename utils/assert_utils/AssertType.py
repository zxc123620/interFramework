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
        if expect_value != actual_value:
            return True, "通过"
        return False, "预期结果与实际结果不一致"

    @staticmethod
    def str_contains(expect_value, actual_value):
        """
        字符串包含判断
        :param expect_value: 预期结果
        :param actual_value: 实际结果
        :return:
        """
        if not actual_value:  # 如果actual_value = false
            return False, "actual_value为FALSE,表示实际结果中没有找到json表达式中的值"
        if expect_value in actual_value:
            return True, "通过"
        return False, "预期结果不包含在实际结果中"

    @staticmethod
    def dict_contains(expect_value: dict, actual_value):
        """
        字典包含判断
        :param expect_value: 预期结果
        :param actual_value: 实际结果
        :return:
        """
        if not actual_value:  # 如果actual_value = false
            return False, "actual_value为FALSE,表示实际结果中没有找到json表达式中的值"
        actual_keys = actual_value.keys()
        for expect_key, value in expect_value.items():
            if expect_key not in actual_keys:  # 判断键是否存在
                # 键不存在
                return False, "预期结果中的字典项在实际结果中不存在"
            else:
                # 键存在
                if value not in actual_value[expect_key]:  # 判断值是否相等
                    # 不相等
                    return False, "预期结果中的值在实际结果中不存在"
        # 前面都没有返回,表示通过
        return True, "通过"


if __name__ == '__main__':
    # getattr(AssertMethod, "equals")(1, 2)
    # print([i.value for i in AssertType])
    assert "1" == "2"
