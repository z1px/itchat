#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/4 0:19
# @Author  : Kevin
# @Site    : 
# @File    : msg.py
# @Software: PyCharm

__author__ = 'Kevin'

# 微信消息监控

import itchat
from itchat.content import *
import time
import re
import os

from common.func import mkdir

path = "./temp/"
mkdir(path=path)

msg_information = {}
face_bug=None  #针对表情包的内容

@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO],isFriendChat=True, isGroupChat=True, isMpChat=True)
def handle_receive_msg(msg):
    global face_bug
    # 接受消息的时间
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(msg_time_rec, "msg：%s" % msg)
    # 在好友列表中查询发送信息的好友昵称
    if "@@" in msg.get("FromUserName"):
        # 群组成员发送消息
        msg_from = itchat.search_friends(userName=msg.get("ActualUserName"))
        if msg_from:
            msg_from = msg_from['NickName'] + "（%s）" % msg_from["RemarkName"] if msg_from["RemarkName"] else msg_from['NickName']
        else:
            msg_from = msg['ActualUserName']

        # 在聊天室列表中查询接收信息的聊天室名称
        msg_to = itchat.search_chatrooms(userName=msg['FromUserName'])
        if msg_to:
            msg_to = msg_to['NickName']
        else:
            msg_to = msg['FromUserName']
        msg_to += "（讨论组）"
    else:
        msg_from = itchat.search_friends(userName=msg['FromUserName'])
        if msg_from:
            msg_from = msg_from['NickName'] + "（%s）" % msg_from["RemarkName"] if msg_from["RemarkName"] else msg_from['NickName']
        else:
            msg = itchat.search_mps(userName=msg['FromUserName'])  # 公众号
            if msg_from:
                msg_from = msg_from['NickName'] + "（公众号）"
            else:
                msg_from = msg['FromUserName']

        # 在好友列表中查询接收信息的好友昵称
        if "@@" in msg.get("ToUserName"):
            msg_to = itchat.search_chatrooms(userName=msg['ToUserName'])
            if msg_to:
                msg_to = msg_to['NickName']
            else:
                msg_to = msg['FromUserName']
            msg_to += "（讨论组）"
        else:
            msg_to = itchat.search_friends(userName=msg['ToUserName'])
            if msg_to:
                msg_to = msg_to["RemarkName"] if msg_to["RemarkName"] else msg_to['NickName']
            else:
                msg_to = msg['ToUserName']

    msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime']))    #信息发送的时间
    msg_id = msg['MsgId']    #每条信息的id
    msg_content = None      #储存信息的内容
    msg_share_url = None    #储存分享的链接，比如分享的文章和音乐
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':     #如果发送的消息是文本或者好友推荐
        msg_content = msg['Text']
        if msg_from != "newsapp":
            print(msg_time, "【%s】给【%s】发送了一条消息：%s" % (msg_from, msg_to, msg_content))
    #如果发送的消息是附件、视屏、图片、语音
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" or msg['Type'] == 'Picture' or msg['Type'] == 'Recording':
        msg_content = msg['FileName']    #内容就是他们的文件名
        msg['Text'](str(path + msg_content))    #下载文件
        if msg['Type'] == "Attachment":
            msg_type = "一个附件"
        elif msg['Type'] == "Video":
            msg_type = "一个视频"
        elif  msg['Type'] == 'Picture':
            msg_type = "一张图片"
        elif  msg['Type'] == 'Recording':
            msg_type = "一条语音"
        else:
            msg_type = "一条消息"
        print(msg_time, "【%s】给【%s】发送了【%s】：%s" % (msg_from, msg_to, msg_type, msg_content))
    elif msg['Type'] == 'Card':    #如果消息是推荐的名片
        msg_content = msg['RecommendInfo']['NickName'] + '的名片'    #内容就是推荐人的昵称和性别
        if msg['RecommendInfo']['Sex'] == 1:
            msg_content += '性别为男'
        else:
            msg_content += '性别为女'
        print(msg_time, "【%s】给【%s】推荐了【%s】名片：%s" % (msg_from, msg_to, msg['RecommendInfo']['NickName'], msg_content))
    elif msg['Type'] == 'Map':    #如果消息为分享的位置信息
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()     #内容为详细的地址
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':     #如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
        msg_content = msg['Text']
        msg_share_url = msg['Url']       #记录分享的url
        print(msg_time, "【%s】给【%s】分享了一条消息：《%s》 %s" % (msg_from, msg_to,msg_content, msg_share_url))
    face_bug=msg_content

    # 将信息存储在字典中，每一个msg_id对应一条信息
    msg_information.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )


##这个是用于监听是否有消息撤回
@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
def information(msg):
    #这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    if '撤回了一条消息' in msg['Content']:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)   #在返回的content查找撤回的消息的id
        old_msg = msg_information.get(old_msg_id)    #得到消息

        # 接受消息的时间
        # msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(msg_time_rec, "msg：%s" % msg)
        # print(msg_time_rec, "old_msg：%s" % old_msg)
        # 聊天对象
        if msg.get("ActualUserName"):
            # 讨论组消息
            msg_from = itchat.search_chatrooms(userName=msg['FromUserName'])
            if msg_from:
                msg_from = msg_from['NickName']
            else:
                msg_from = msg['FromUserName']
            msg_from = msg_from + "（讨论组）"
            msg_to = msg.get("ActualUserName")
        else:
            # 好友消息
            msg_from = itchat.search_friends(userName=msg.get("FromUserName"))
            if msg_from:
                msg_from = msg_from["RemarkName"] if msg_from["RemarkName"] else msg_from['NickName']
            else:
                msg_from = msg['FromUserName']

            if msg["Text"] == "你撤回了一条消息":
                msg_to = msg["ToUserName"]
            else:
                msg_to = msg['FromUserName']

        # 在好友列表中查询撤回信息的好友昵称
        msg_to = itchat.search_friends(userName=msg_to)
        if msg_to:
            msg_to = msg_to["RemarkName"] if msg_to["RemarkName"] else msg_to['NickName']
        else:
            msg_to = msg['ToUserName']

        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), old_msg)
        if len(old_msg_id)<11:  #如果发送的是表情包
            itchat.send_file(face_bug, toUserName='filehelper')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), face_bug)
        else:  #发送撤回的提示给文件助手

            msg_body = "告诉你一个秘密~" + "\n" \
                       + "与【"+ msg_from +"】的对话中，【"+ msg_to +"】撤回了一条" + old_msg.get("msg_type") + " 消息" + "\n" \
                       + "消息发送时间" + old_msg.get('msg_time') + "，撤销时间"+ old_msg.get('msg_time_rec') +"\n" \
                       + "撤回了什么 ⇣" + "\n" \
                       + r"" + old_msg.get('msg_content')
            #如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')

            # 将撤回消息发送到文件助手
            itchat.send_msg(msg_body, toUserName='filehelper')
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" or old_msg["msg_type"] == "Recording" or old_msg["msg_type"] == "Video" or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (path + old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(path + old_msg['msg_content'])
                msg_body += "\n就是这个文件➣ " + old_msg['msg_content']

            print("【消息撤回】：", msg_body + "\n【消息撤回END】")
            # 删除字典旧消息
            msg_information.pop(old_msg_id)

itchat.auto_login(hotReload=True)
itchat.run()