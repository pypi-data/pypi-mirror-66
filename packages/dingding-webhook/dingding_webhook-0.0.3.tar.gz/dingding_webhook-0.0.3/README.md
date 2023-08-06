# dingding webhook

This is a simple python api package to send your own message by dingding robot.




#Installation

```bash
pip install dingding_webhook
```



#Usage


send msg

```python
import dingding_webhook.webhook as dingding_webhook


webhook_url="xxx"  # your dingding robot webhook

content = "test text msg"

dingding_webhook.send_text(webhook_url,
                            content, 
                            atMobiles=[], 
                            isAtAll=False)

```


###Examples


- text类型
```python
# text类型
# 参数     参数类型   必须    说明
# msgtype   String   是     消息类型，此时固定为：text
# content   String   是     消息内容
# atMobiles Array    否    被@人的手机号(在content里添加@人的手机号)
# isAtAll   bool     否    @所有人时：true，否则为：false
```
send_text(post_url, content, atMobiles=[], isAtAll=False)


- link类型

```python
# 参数     参数类型   必须    说明
# msgtype   String    是    消息类型，此时固定为：link
# title     String    是    消息标题
# text      String    是    消息内容。如果太长只会部分展示
# messageUrl String   是    点击消息跳转的URL
# picUrl    String    否 图片URL
```
send_link(post_url, title, text, picUrl, msgUrl)

- markdown类型
```python
# 参数     参数类型   必须    说明
# msgtype   String   是     消息类型，此时固定为：markdown
# title     String   是     首屏会话透出的展示内容
# text      String   是     markdown格式的消息
# atMobiles Array    否    被@人的手机号(在content里添加@人的手机号)
# isAtAll   bool     否    @所有人时：true，否则为：false
```
send_markdown(post_url, title, text, atMobiles=[], isAtAll=False)

- 整体跳转ActionCard类型
```python
# 参数      类型      必选      说明
# msgtype   string    true    此消息类型为固定actionCard
# title     string    true    首屏会话透出的展示内容
# text      string    true    markdown格式的消息
# btns.btnOrientation  string  false  "0"-按钮竖直排列，"1"-按钮横向排列
# btns.buttons    [{               "title": "内容不错",         "actionURL": "https://www.dingtalk.com/"            },
#           {       "title": "不感兴趣",                "actionURL": "https://www.dingtalk.com/"         }      ]
# hideAvatar      string  false  "0"-正常发消息者头像，"1"-隐藏发消息者头像
```
send_actionCard(post_url, title, text, btns, hideAvatar="0")


- FeedCard类型
```python
# FeedCard类型
# 参数      类型      必选      说明
# msgtype string      true    此消息类型为固定feedCard
# cardList array      true      
# 
# cardList[0].title   string      true    单条信息文本
# cardList[0].messageURL  string  true    点击单条信息到跳转链接
# cardList[0].picURL  string      true    单条信息后面图片的URL
```
send_feedCard(post_url, cardList)

###Documentation

more docs see

[dingding doc](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)

