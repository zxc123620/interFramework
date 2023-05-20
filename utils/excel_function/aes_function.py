#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES

from config import PWD


class EncryptDate:
    def __init__(self):
        self.key = PWD.encode("utf-8")  # 初始化密钥
        self.length = AES.block_size  # 初始化数据块大小
        self.aes = AES.new(self.key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
        # Base64是网络上最常见的用于传输8Bit字节码的编码方式之一
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        msg = self.aes.decrypt(res).decode("utf8")
        return self.unpad(msg)


if __name__ == '__main__':
    print("============加密==================")
    key = "1234567812345678"  # key 密码,服务器指定
    data = "tony"  # 数据
    eg = EncryptDate()  # 这里密钥的长度必须是16的倍数
    res = eg.encrypt(str(data))
    print(res, end='')
    print("\n============解密==================")
    data = "XbXHJrNLwoTVcyfqM9eTgQ=="  # 数据
    res = eg.decrypt(str(data))
    print(res, end='')
