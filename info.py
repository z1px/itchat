#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/4 0:34
# @Author  : Kevin
# @Site    : 
# @File    : info.py
# @Software: PyCharm

__author__ = 'Kevin'

# 用itchat爬取微信好友基本信息
# http://blog.csdn.net/zhanshirj/article/details/74166303

import itchat
import pandas as pd

# 登陆微信
# hotReload=True  # 使用这个属性，生成一个静态文件itchat.pkl，用于存储登陆的状态。
itchat.auto_login(hotReload=True)

# 好友基本信息
friends = itchat.get_friends(update=True)

NickName = friends[0].NickName #获取自己的昵称

for user in friends:
    print()
    print('user.NickName:',user.NickName)
    print('user.Sex:', user.Sex)
    print('user.City:', user.City)
    print('user.Signature:',user.Signature)
    print('user.Province:', user.Province)

### 好友数量
number_of_friends = len(friends)

# pandas可以把据处理成 DataFrame，这极大方便了后续分析。
df_friends = pd.DataFrame(friends)

### 分析好友性别
# 男性为1；女性为2；未知为0；

# 获取性别信息：
Sex = df_friends.Sex

# pandas为Series提供了一个value_counts()方法，可以更方便统计各项出现的次数：
Sex_count = Sex.value_counts() #defaultdict(int, {0: 31, 1: 292, 2: 245})

# 好友都来自什么地方
# 先来看Province
Province = df_friends.Province
Province_count = Province.value_counts()
Province_count = Province_count[Province_count.index!=''] #有一些好友地理信息为空，过滤掉这一部分人。

# 再来看City
City = df_friends.City #[(df_friends.Province=='北京') | (df_friends.Province=='四川')]
City_count = City.value_counts()
City_count = City_count[City_count.index!='']

# 把如上基本信息打印并发到自己的文件助手
msg_body = '你共有%d个好友,其中有%d个男生，%d个女生，%d未显示性别。\n\n' %(number_of_friends, Sex_count[1], Sex_count[2], Sex_count[0]) +\
           '你的朋友主要来自省份：%s(%d)、%s(%d)和%s(%d)。\n\n' %(Province_count.index[0],Province_count[0],Province_count.index[1],Province_count[1],Province_count.index[2],Province_count[2]) + \
           '主要来自这些城市：%s(%d)、%s(%d)、%s(%d)、%s(%d)、%s(%d)和%s(%d)。'%(City_count.index[0],City_count[0],City_count.index[1],City_count[1],City_count.index[2],City_count[2],City_count.index[3],City_count[3],City_count.index[4],City_count[4],City_count.index[5],City_count[5])

print(msg_body)

# 将基本信息发送到文件助手
itchat.send_msg(msg_body, toUserName='filehelper')

