# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:44:15
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-19 11:01:32
# @github: https://github.com/longfengpili

from conf import APPID, APIKEY, APISECRET
from xinghuo.chat import XinghuoChat
from xinghuo.contents import Content, Contents


if __name__ == "__main__":
    appid = APPID
    apikey = APIKEY
    apisecret = APISECRET
    sparkurl = 'wss://spark-api.xf-yun.com/v2.1/chat'

    content1 = Content(**{'role': 'user', 'content': '介绍下pandas'})
    contents = Contents(content1)

    xhchat = XinghuoChat(appid, apikey, apisecret, sparkurl)
    xhchat.chat_stream(contents)
    
