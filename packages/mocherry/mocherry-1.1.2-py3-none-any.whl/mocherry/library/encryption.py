#!/usr/bin/env python

import string
from random import choice
from Crypto.Cipher import AES
import base64

class EncryptionHandler:
    def __init__(self, key=None):
        self.key = key
        self.EOD = '`%EofD%`'

    def encrypt(self, s, base64_encoded=False):
        key = self.key
        obj = AES.new(key)
        datalength = len(s) + len(self.EOD)
        if datalength < 16:
            saltlength = 16 - datalength
        else:
            saltlength = 16 - datalength % 16
        ss = ''.join([s, self.EOD, self.__genstring(saltlength)])
        cipher = obj.encrypt(ss)
        # encode raw AES cypher to b64 encoding
        if base64_encoded is True:
            cipher = base64.b64encode(cipher)
        return cipher


    def decrypt(self, cipher, base64_encoded=False):
        key = self.key
        obj = AES.new(key)
        # decode to raw AES cypher from b64 encoding
        if base64_encoded is True:
            cipher = base64.b64decode(cipher)
        ss = obj.decrypt(cipher)
        return ss.split(self.EOD)[0]


    def __genstring(self, length=16, chars=string.printable):
        return ''.join([choice(chars) for i in range(length)])