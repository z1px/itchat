#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/3 23:44
# @Author  : Kevin
# @Site    : 
# @File    : weixin.py
# @Software: PyCharm

__author__ = 'Kevin'

#获取个人微信号中朋友信息
#导入itchat包
import itchat

#获取个人微信号好友信息
if __name__=="__main__":
    # #登录个人微信，扫码登录
    # itchat.login()
    # #爬取自己好友相关信息
    # friends=itchat.get_friends(update=False)[0:]
    # #设置需要爬取的信息字段
    # result=[('RemarkName','备注'),('NickName','微信昵称'),('Sex','性别'),('City','城市'),('Province','省份'),('ContactFlag','联系标识'),('UserName','用户名'),('SnsFlag','渠道标识'),('Signature','个性签名')]
    # for user in friends:
    #     with open('myFriends.txt','a',encoding='utf8') as fh:
    #         fh.write("-----------------------\n")
    #     for r in result:
    #         with open('myFriends.txt','a',encoding='utf8') as fh:
    #             fh.write(r[1]+":"+str(user.get(r[0]))+"\n")

    itchat.auto_login()
    print("get_contact：", itchat.get_contact(update=False))
    print("get_friends：", itchat.get_friends(update=False))
    print("get_mps：", itchat.get_mps(update=False))
    print("get_chatrooms：", itchat.get_chatrooms(update=False, contactOnly=False))
    print("get_head_img：", itchat.get_head_img(userName=None, chatroomUserName=None, picDir=None))

    print("完成")