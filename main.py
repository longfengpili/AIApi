# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:44:15
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-26 18:43:53
# @github: https://github.com/longfengpili

from conf import APPID, APIKEY, APISECRET
from xinghuo.chat import XinghuoChat
from xinghuo.contents import Content, Contents


if __name__ == "__main__":
    appid = APPID
    apikey = APIKEY
    apisecret = APISECRET

    content1 = Content(**{'role': 'user', 'content': '介绍下pandas'})
    contents = Contents(content1)

    xhchat = XinghuoChat(appid, apikey, apisecret)
    # xhchat.chat(contents)
    xhchat.chat_stream(contents)
