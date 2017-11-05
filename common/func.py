#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/20 上午10:29
# @Author  : Kevin
# @Site    : 
# @File    : func.py
# @Software: PyCharm

__author__ = 'Kevin'

import os
import time
import ast
import hashlib


# 日志打印
def log(*args, sep=' ', end='\n', file=None):
    try:
        print("%s   " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, sep=sep, end=end, file=file)
    except:
        print("%s   " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "日志打印失败", sep=sep, end=end, file=file)

# 递归创建文件夹
def mkdir(path):
    try:
        if not os.path.isdir(path):
            os.makedirs(path)  # 递归创建目录
        return True
    except:
        return False

# 编码转化
def decode(data):
    try:
        if isinstance(data, bytes):
            data = data.decode("utf-8")
    except:
        pass
    return data

# 编码转化
def encode(data):
    try:
        if not isinstance(data, bytes):
            data = data.encode("gb2312")
    except:
        pass
    return data

# 字符串转dict
def literal_eval(data):
    if not isinstance(data, dict):
        if isinstance(data, bytes):
            data = decode(data)
        try:
            data = ast.literal_eval(data)
        except:
            pass
    return data

# MD5加密
def md5(data):
    md5 = hashlib.md5()
    md5.update(encode(data))
    return md5.hexdigest()