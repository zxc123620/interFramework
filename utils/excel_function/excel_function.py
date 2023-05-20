"""
用于excel可调用函数
"""
import hashlib

from utils.excel_function.aes_function import EncryptDate
from utils.excel_function.rsa_function import Rsa

eg = EncryptDate()
rsaer = Rsa()


class ExcelFunction:
    @staticmethod
    def get_id(a, *args):
        return 1

    @staticmethod
    def md5(data: str, *args):
        """
        md5加密
        Args:
            data: 需要加密的数据

        Returns:

        """
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    @staticmethod
    def aes_en(content: str, *args):
        """
        aes加密
        Args:
            content: 加密内容
        Returns:
        """
        return eg.encrypt(content)

    @staticmethod
    def aes_de(content: str, *args):
        """
        aes 解密
        Args:
            content:

        Returns:

        """
        return eg.decrypt(content)

    @staticmethod
    def rsa_en(content: str, *args):
        """
        rsa加密
        Args:
            content: 加密内容

        Returns:

        """
        return rsaer.encrypt(content)

    @staticmethod
    def rsa_de(content: str, *args):
        """
        rsa解密
        Args:
            content: 解密

        Returns:

        """
        return rsaer.decrypt(content)

    @staticmethod
    def f_int(i):
        """
        int转换
        Args:
            i:

        Returns:

        """
        return int(i)
