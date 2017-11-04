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

msg = "我看下"

ToUserName = '@cc112089a58192af5e279827198a4e66d7c1ed24b3042eebff0640b198a5a209'
# 将签名词云发送到文件助手
itchat.send(msg=msg, toUserName=ToUserName)