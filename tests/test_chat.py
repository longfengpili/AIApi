# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-20 14:05:00
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-10-27 17:31:59
# @github: https://github.com/longfengpili

from xinghuo.config import AIConfig
from xinghuo.chat import XinghuoChat
from xinghuo.contents import Content, Contents


class TestChat:

    def setup_method(self, method):
        aiconf = AIConfig.load('xinghuo')
        self.content = Content(**{'role': 'user', 'content': '介绍下pandas'})
        self.contents = Contents(self.content)
        self.xhchat = XinghuoChat(aiconf.appname, aiconf.appid, aiconf.appkey, aiconf.appsecret)

    def teardown_method(self, method):
        pass

    def test_chat(self):
        sid, contents = self.xhchat.chat(self.contents)
        print(sid)
        print(contents)

    def test_chat_stream(self):
        contents = self.xhchat.chat_stream(self.contents)
        print(contents)
