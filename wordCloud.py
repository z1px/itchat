#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/4 16:18
# @Author  : Kevin
# @Site    : 
# @File    : wordCloud.py
# @Software: PyCharm

__author__ = 'Kevin'

# 微信好友签名词云

import itchat

from common.func import mkdir


# 登陆微信
# hotReload=True  # 使用这个属性，生成一个静态文件itchat.pkl，用于存储登陆的状态。
itchat.auto_login(hotReload=True)

friends=itchat.get_friends(update=True)[0:]

NickName = friends[0].NickName #获取自己的昵称

# 除去特殊字符
import re

siglist = []
for i in friends:
    signature = i["Signature"].strip().replace('span','').replace('class','').replace('emoji','').replace('\n','')
    rep = re.compile("1f\d+\w*|[<>/=]")
    signature = rep.sub("", signature)
    siglist.append(signature)
text = "".join(siglist)

#分词
import jieba

wordlist = jieba.cut(text, cut_all=True)
word_space_split = " ".join(wordlist)
print(word_space_split)

#绘制词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import PIL.Image as Image

coloring = np.array(Image.open("./wechat/wechat.jpg"))#自定义词云的图片
my_wordcloud = WordCloud(background_color="white", max_words=2000, mask=coloring, max_font_size=60, random_state=42, font_path='C:/windows/fonts/SimHei.ttf',scale=2).generate(word_space_split) # wget http://labfile.oss.aliyuncs.com/courses/756/DroidSansFallbackFull.ttf中文字符文件

# 程序绘制图片
image_colors = ImageColorGenerator(coloring)
plt.figure("wechat_cloud")
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
plt.close()

#保存图片
path_image = "./image/"
mkdir(path=path_image)
file_name_p =  path_image + 'wechat_cloud.jpg'
my_wordcloud.to_file(file_name_p)

# 将签名词云发送到文件助手
itchat.send_image(file_name_p, 'filehelper')

