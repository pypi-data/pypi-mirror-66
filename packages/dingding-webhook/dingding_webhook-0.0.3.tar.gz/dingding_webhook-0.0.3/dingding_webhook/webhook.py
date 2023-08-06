# -*- coding: utf-8 -*-
import requests


# text类型
# 参数     参数类型   必须    说明
# msgtype   String   是     消息类型，此时固定为：text
# content   String   是     消息内容
# atMobiles Array    否    被@人的手机号(在content里添加@人的手机号)
# isAtAll   bool     否    @所有人时：true，否则为：false
def send_text(post_url, content, atMobiles=[], isAtAll=False):
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "atMobiles": atMobiles,
            "isAtAll": isAtAll
        }
    }
    r = requests.post(post_url, json=data)
    response = r.json()
    return response


# link类型
# 参数     参数类型   必须    说明
# msgtype   String    是    消息类型，此时固定为：link
# title     String    是    消息标题
# text      String    是    消息内容。如果太长只会部分展示
# messageUrl String   是    点击消息跳转的URL
# picUrl    String    否 图片URL
def send_link(post_url, title, text, picUrl, msgUrl):
    data = {
        "msgtype": "link",
        "link": {
            "text": text,
            "title": title,
            "picUrl": picUrl,
            "messageUrl": msgUrl
        }
    }
    r = requests.post(post_url, json=data)
    response = r.json()
    return response


# markdown类型
# 参数     参数类型   必须    说明
# msgtype   String   是     消息类型，此时固定为：markdown
# title     String   是     首屏会话透出的展示内容
# text      String   是     markdown格式的消息
# atMobiles Array    否    被@人的手机号(在content里添加@人的手机号)
# isAtAll   bool     否    @所有人时：true，否则为：false
def send_markdown(post_url, title, text, atMobiles=[], isAtAll=False):
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        },
        "at": {
            "atMobiles": atMobiles,
            "isAtAll": isAtAll
        }
    }
    r = requests.post(post_url, json=data)
    response = r.json()
    return response


# 整体跳转ActionCard类型
# 参数      类型      必选      说明
# msgtype   string    true    此消息类型为固定actionCard
# title     string    true    首屏会话透出的展示内容
# text      string    true    markdown格式的消息
# btns.btnOrientation  string  false  "0"-按钮竖直排列，"1"-按钮横向排列
# btns.buttons    [{               "title": "内容不错",         "actionURL": "https://www.dingtalk.com/"            },
#           {       "title": "不感兴趣",                "actionURL": "https://www.dingtalk.com/"         }      ]
# hideAvatar      string  false  "0"-正常发消息者头像，"1"-隐藏发消息者头像
def send_actionCard(post_url, title, text, btns, hideAvatar="0"):
    data = {
        "actionCard": {
            "title": title,
            "text": text,
            "hideAvatar": hideAvatar,
            "btnOrientation": btns.btnOrientation,
            "btns": btns.buttons
        },
        "msgtype": "actionCard"
    }
    r = requests.post(post_url, json=data)
    response = r.json()
    return response


# FeedCard类型
# 参数      类型      必选      说明
# msgtype string      true    此消息类型为固定feedCard
# cardList[0].title   string      true    单条信息文本
# cardList[0].messageURL  string  true    点击单条信息到跳转链接
# cardList[0].picURL  string      true    单条信息后面图片的URL
def send_feedCard(post_url, cardList):
    data = {
        "feedCard": {
            "links": cardList
        },
        "msgtype": "feedCard"
    }
    r = requests.post(post_url, json=data)
    response = r.json()
    return response