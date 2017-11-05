#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/4 23:52
# @Author  : Kevin
# @Site    : 
# @File    : helper.py
# @Software: PyCharm

__author__ = 'Kevin'

# 用itchat爬取微信好友基本信息
# http://blog.csdn.net/zhanshirj/article/details/74166303

import itchat

# 登陆微信
# hotReload=True  # 使用这个属性，生成一个静态文件itchat.pkl，用于存储登陆的状态。
itchat.auto_login(hotReload=True)

# print(itchat.search_chatrooms(userName="@@9e0d639cb86e12208ab424747ceb8fa8d70fe913d882f5d51ad4d6558aebfaae"))

# msg = "https://github.com/z1px/itchat.git"

# ToUserName = 'filehelper' # 文件助手
# ToUserName = '@@9c8fb78330c066b4b81d8c4c9a667881ea949dcb9d93be2ff4e9deba3de23710' # 老表讨论组
# 将签名词云发送到好友
# itchat.send(msg=msg, toUserName=ToUserName)