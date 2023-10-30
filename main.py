# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:44:15
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-10-30 18:49:55
# @github: https://github.com/longfengpili

from xinghuo.config import AIConfig
from xinghuo.chat import XinghuoChat
from xinghuo.contents import Content, Contents


if __name__ == "__main__":
    aiconf = AIConfig.load('xinghuo')
    question = '介绍下pandas'

    xhchat = XinghuoChat(aiconf.appname, aiconf.appid, aiconf.appkey, aiconf.appsecret)
    sid, contents = xhchat.chat(question)
    print(sid, contents)
    xhchat.chat_stream(contents)
