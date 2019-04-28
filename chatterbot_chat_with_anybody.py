#coding=utf8
import itchat
import time
import json 
import time
import numpy as np 
import os 
import random
from itchat.content import *
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

# 实现一个chatterbot
chatbot = ChatBot('final',storage_adapter="chatterbot.storage.SQLStorageAdapter")
storage_adapter={
        "import_path": "chatterbot.storage.SQLStorageAdapter",
        "database_uri": "sqlite:///test.sqlite4"
    }
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.chinese")
# 用来存储获得的语料，不需要的话可以注释掉
f = open('xiaobing','a+',encoding='utf8')

# 回复消息
def reply(sen):
    rep = chatbot.get_response(sen)
    print(rep)
    return str(rep)

# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息

@itchat.msg_register(TEXT, isFriendChat=False, isGroupChat=False,isMpChat=True)
''' isFriendChat表示是否是好友的消息
    isGroupChat代表是否是群聊消息
    isMpChat代表是否是公众号 
 '''
def text_reply(msg):
    # 防止小冰炸掉
    time.sleep(2.5)
    # 如果消息来自小冰
    # 当然这可以改成任何人，注意修改上述注册中的参数
    if msg['FromUserName'] == userName:
        rep = reply(msg['Text'])
        # 收集语料
        f.write(msg['Text']+'\n')
        f.write(rep+'\n')
        # 回复给好友
        return rep

if __name__ == '__main__':
    itchat.auto_login()
    # 搜索关注的公众号 找到小冰
    mps = itchat.get_mps()
    mps = itchat.search_mps(name='小冰')
    userName = mps[0]["UserName"]
    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()
    f.close()