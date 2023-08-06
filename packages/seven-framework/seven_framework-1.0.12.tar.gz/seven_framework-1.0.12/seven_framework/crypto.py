# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-04-16 14:38:22
@LastEditTime: 2020-04-25 22:53:42
@LastEditors: ChenXiaolei
@Description: 
"""
import base64
import binascii
from Crypto.Cipher import AES


class CryptoHelper:
    """
    @description: 加密帮助类
    """
    @classmethod
    def md5_encrypt(self, source, salt=""):
        """
        @description: md5加密，支持加盐算法
        @param source: 需加密的字符串
        @param salt: 加盐算法参数值
        @return: md5加密后的字符串
        @last_editors: ChenXiaolei
        """
        if not source.strip():
            return ""
        import hashlib
        encrypt = hashlib.md5()
        encrypt.update(
            (source + salt).encode('utf-8')
        )  # 参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
        md5value = encrypt.hexdigest()
        return md5value

    @classmethod
    def md5_encrypt_int(self, source, salt=""):
        """
        @description: md5加密，返回数值
        @param source: 需加密的字符串
        @param salt: 加盐算法参数值
        @return: md5加密后的数值
        @last_editors: ChenXiaolei
        """
        md5_16 = self._convert_md5(self.md5_encrypt(source, salt))
        hash_code_start = int.from_bytes(md5_16[0:8],
                                         byteorder='little',
                                         signed=True)
        hash_code_end = int.from_bytes(md5_16[8:16],
                                       byteorder='little',
                                       signed=True)
        return hash_code_start ^ hash_code_end

    @classmethod
    def _convert_md5(self, origin):
        """
        @description: md5字符串转16进制数组
        @param origin: 原md5字符串
        @return: 16进制数组
        @last_editors: ChenXiaolei
        """
        result = []
        s = ""
        for i in range(len(origin)):
            s += origin[i]
            if i % 2 != 0:
                int_hex = int(s, 16)
                result.append(int_hex)
                s = ""

        return result

    @classmethod
    def base64_encode(self, source):
        """
        @description: base64加密
        @param source: 需加密的字符串
        @return: 加密后的字符串
        @last_editors: ChenXiaolei
        """
        if not source.strip():
            return ""
        import base64
        encode_string = base64.b64encode(source.encode(encoding='utf-8'))
        return encode_string

    @classmethod
    def base64_decode(self, source):
        """
        @description: base64解密
        @param source: 需加密的字符串
        @return: 解密后的字符串
        @last_editors: ChenXiaolei
        """
        if not source.strip():
            return ""
        import base64
        decode_string = base64.b64decode(source)
        return decode_string

    @classmethod
    def aes_encrypt(self, data, password):
        """
        @description: AES加密,ECB & PKCS7
        @param {type} 
        @return: 
        @last_editors: ChenXiaolei
        """
        if isinstance(password, str):
            password = password.encode('utf8')

        bs = AES.block_size
        pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        cipher = AES.new(password, AES.MODE_ECB)
        data = cipher.encrypt(pad(data).encode('utf8'))
        encrypt_data = binascii.b2a_hex(data)  # 输出hex
        encrypt_data = base64.b64encode(data)  # 输出Base64格式
        return encrypt_data.decode('utf8')

    @classmethod
    def aes_decrypt(self, decrData, password):
        """
        @description: 
        @param {type} 
        @return: 
        @last_editors: ChenXiaolei
        """
        if isinstance(password, str):
            password = password.encode('utf8')

        cipher = AES.new(password, AES.MODE_ECB)
        plain_text = cipher.decrypt(binascii.a2b_hex(decrData))
        return plain_text.decode('utf8').rstrip('\0')
