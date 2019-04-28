#coding=utf8
import itchat
import time
import json 
import numpy as np 
import os 
import random
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
'''
基于图灵机器人的智能聊天机器人。
需要先自己去注册机器人
注册网址:http://www.tuling123.com
'''

import json
import urllib.request

# 获得语料，如果不需要，可以注释掉
f = open("data_from_turing.txt",'a+',encoding = 'utf8')
api_url = "http://openapi.tuling123.com/openapi/api/v2"

def reply(sen):
'''
    调用图灵机器人接口，返回回复信息。
'''
    text_input = sen 
    req = {
        "perception":
        {
            "inputText":
            {
                "text": text_input # 输入
            },

            "selfInfo":
            {
                "location":
                {
                    "city": "北京", # 改成自己的地址 
                    "province": "海淀区",  # 改不改无所谓
                    "street": "清华大学"
                }
            }
        },

        "userInfo": 
        {
            "apiKey": "a8f715e3fb054962ad8703751a727ad2", #这里修改成你自己的apikey
            "userId": "OnlyUseAlphabet" #不用管
        }
    }
    print(text_input)
    # 将字典格式的req编码为utf8
    req = json.dumps(req).encode('utf8')

    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)

    intent_code = response_dic['intent']['code']
    results_text = response_dic['results'][0]['values']['text']
    return results_text

# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
@itchat.msg_register('Text')
def text_reply(msg):
    # 当消息不是由自己发出的时候
    if not msg['FromUserName'] == myUserName:
        rep = reply(msg['Text'])
        # 增加语料
        f.write(msg["Text"]+'\n')
        f.write(rep+'\n')
        # 回复给好友
        return '假ph:' + rep

if __name__ == '__main__':
    itchat.auto_login()

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()
    f.close()