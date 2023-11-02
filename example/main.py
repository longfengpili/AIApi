# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:44:15
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-02 11:46:45
# @github: https://github.com/longfengpili

from xinghuo.config import AIConfig
from xinghuo.chat import XinghuoChat
from xinghuo.contents import Content, Contents

# aiconf = AIConfig.load('1')
# print(aiconf)

if __name__ == "__main__":
    aiconf = AIConfig.load('xinghuo')
    question = '介绍下pandas'

    xhchat = XinghuoChat(aiconf.appname, aiconf.appid, aiconf.apikey, aiconf.apisecret)
    sid, contents = xhchat.chat(question)
    print(sid, contents)
    # xhchat.chat_stream(contents)
