# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:44:15
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-02 11:38:57
# @github: https://github.com/longfengpili

from xinghuo.config import AIConfig
from xinghuo.chat import XinghuoChat
from xinghuo.contents import Content, Contents

# aiconf = AIConfig.load('1')
# print(aiconf)

if __name__ == "__main__":
    APPID = "9d1114e8"
    APIKEY = "568c0d48cb4a54b17edcc89e86f03600"
    APISECRET = "MWM4ZjlhNWM3NTJmNTNlYzZhYzQ1YTY2"
    # aiconf = AIConfig.load('xinghuo')
    aiconf = AIConfig('xinghuo', APPID, APIKEY, APISECRET)
    dumpfile = aiconf.dump()
    # print(dumpfile)
    # print(aiconf)
    question = '介绍下pandas'

    xhchat = XinghuoChat(aiconf.appname, aiconf.appid, aiconf.apikey, aiconf.apisecret)
    sid, contents = xhchat.chat(question)
    print(sid, contents)
    # xhchat.chat_stream(contents)
