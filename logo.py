#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/4 17:40
# @Author  : Kevin
# @Site    : 
# @File    : logo.py
# @Software: PyCharm

__author__ = 'Kevin'

import itchat
import math
from PIL import Image
import os

from common.func import mkdir

# hotReload=True  # 使用这个属性，生成一个静态文件itchat.pkl，用于存储登陆的状态。
itchat.auto_login(hotReload=True)

friends = itchat.get_friends(update=True)[0:]

path = './logo/'
mkdir(path=path)

for item in friends:
    # 可以打印item来看其中具体是什么内容，有什么字段
    img = itchat.get_head_img(userName=item['UserName'])
    if not item['RemarkName']:
        item['RemarkName'] = item['NickName']
    with open(path + item['RemarkName'] + '.jpg', 'wb') as f:
        f.write(img)

# 获取好友昵称和签名
info = [(item['RemarkName'] if item['RemarkName'] else item['NickName'], item['Signature']) for item in friends]

# 获取文件夹中所有的图片
ls = os.listdir(path)
img_num = len(ls)
# 大图最大长宽
max_width = 640
# 每行放几张
lines = math.ceil(math.sqrt(img_num))
# 每张小图片宽
size = int(max_width/lines)
# 大图长宽
width = size*lines

# 画一个大图，用来放小头像
image = Image.new('RGBA', (width, width))
x = 0
y = 0
for i in range(0, len(ls)):
    try:
        img = Image.open(path + info[i][0] + '.jpg')
    except IOError:
        print(path + info[i][0] + '.jpg打开失败！！！')
    else:
        img = img.resize((size, size), Image.ANTIALIAS)
        # 向指定位置放缩小后的图片
        image.paste(img, (x * size, y * size))
        x += 1
        if x == lines:
            x = 0
            y += 1

# 调用操作系统自带的图片浏览器来打开图片
# image.show()

# 程序绘制图片
import matplotlib.pyplot as plt
plt.figure("logo")
plt.imshow(image)
plt.axis("off")
plt.show()
plt.close()

#保存图片
path_image = "./image/"
mkdir(path=path_image)
logo = path_image + "logo.jpg"
image.save(logo)

# 通过文件助手发给自己
itchat.send_image(logo, 'filehelper')
