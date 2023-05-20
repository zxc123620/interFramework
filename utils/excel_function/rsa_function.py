#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import rsa
from config import ROOT_PATH

#
# # 秘钥的位数, 可以自定义指定, 例如: 128、256、512、1024、2048等
#
# (pubkey, privkey) = rsa.newkeys(512)
# # # 生成公钥
# pub = pubkey.save_pkcs1()
# with open(ROOT_PATH + 'public.pem', 'wb') as f:
#     f.write(pub)
#
# # # 生成私钥
# pri = privkey.save_pkcs1()
# with open(ROOT_PATH + 'private.pem', 'wb') as f:
#     f.write(pri)

with open(ROOT_PATH + '/public.pem', 'rb') as f:
    pub_str = f.read()

# # 生成私钥
with open(ROOT_PATH + '/private.pem', 'rb') as f:
    priv_str = f.read()


class Rsa:
    def __init__(self):
        self.pub_key = rsa.PublicKey.load_pkcs1(pub_str)
        self.priv_key = rsa.PrivateKey.load_pkcs1(priv_str)

    def encrypt(self, text):
        # rsa加密 最后把加密字符串转为base64
        text = text.encode("utf-8")
        cryto_info = rsa.encrypt(text, self.pub_key)
        cipher_base64 = base64.b64encode(cryto_info)
        cipher_base64 = cipher_base64.decode()
        return cipher_base64

    def decrypt(self, text):
        # rsa解密 返回解密结果
        cryto_info = base64.b64decode(text)
        talk_real = rsa.decrypt(cryto_info, self.priv_key)
        res = talk_real.decode("utf-8")
        return res


if __name__ == "__main__":
    rsaer = Rsa()
    info = rsaer.encrypt('展昭')
    print('加密:', info)
    print('解密:', rsaer.decrypt(info))
    # 加密: HcbXuD4kkHKzwC4h2G7S2EPNG5O1RnOrisstGF1lgi4=
    # 解密: 展昭
