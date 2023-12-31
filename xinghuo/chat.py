# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:29:34
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-01 11:03:17
# @github: https://github.com/longfengpili


import json
from websockets.sync.client import connect
from websockets import ConnectionClosedOK

from .auth import XingHuoAuth
from .contents import Content, Contents

XINGHUOAPI = {
    'api_v1': {
        'url': 'wss://spark-api.xf-yun.com/v1.1/chat',
        'domain': 'general'
    },
    'api_v2': {
        'url': 'wss://spark-api.xf-yun.com/v2.1/chat',
        'domain': 'generalv2'
    },
    'api_v3': {
        'url': 'wss://spark-api.xf-yun.com/v3.1/chat',
        'domain': 'generalv3'
    }
}


class XinghuoChat(XingHuoAuth):

    def __init__(self, appname: str, appid: str, apikey: str, apisecret: str, apiver: str = 'v3', **kwargs: dict):
        self.appname = appname
        self.appid = appid
        self.domain = XINGHUOAPI.get(f"api_{apiver}").get('domain')
        self.sparkurl = XINGHUOAPI.get(f"api_{apiver}").get('url')
        self.kwargs = kwargs
        self.sid = ''
        self.answer = ''
        self.contents = Contents()
        super(XinghuoChat, self).__init__(apikey, apisecret, self.sparkurl)

    @property
    def websocket(self):
        websocket = connect(self.auth_url)
        return websocket

    def build_message(self, contents: Contents, uid: str = '123'):
        contents = contents.chatdata
        data = {
            "header": {
                "app_id": self.appid,
                "uid": uid
            },
            "parameter": {
                "chat": {
                    "domain": self.domain,
                    "temperature": 0.5,
                    "max_tokens": 2048,
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": contents
                }
            }
        }
        return json.dumps(data, ensure_ascii=False)

    def parse_response(self, response: str):
        # print(response)
        usage = {}
        data = json.loads(response)
        code = data['header']['code']
        sid = data['header']['sid']

        if code != 0:
            self.websocket.close()
            raise ValueError(f'请求错误: {code}, {data}')

        if sid != self.sid:
            self.sid = sid
            self.answer = ''

        choices = data['payload']['choices']
        status = choices['status']
        content = choices['text'][0]['content']
        self.answer += content

        end = '\n' if status == 2 else ''
        print(content, end=end)
        if status == 2:
            usage = data['payload']['usage']['text']

        return sid, usage

    def chat(self, question: str, contents: Contents = None, uid: str = '123', is_show_content: bool = False):
        question = Content(**{'role': 'user', 'content': question})
        contents = contents if contents else Contents()
        contents.append(question)

        if is_show_content:
            print(contents)
        print(">>>>>>>>>>>>Answer:\n")

        websocket = self.websocket
        message = self.build_message(contents)
        websocket.send(message)

        while True:
            try:
                response = websocket.recv()
                sid, usage = self.parse_response(response)
            except ConnectionClosedOK:
                # print(sid, usage)
                break
            
        answer = Content('assistant', self.answer, sid=sid, **usage)
        contents.append(answer)

        return sid, contents

    def chat_stream(self, question: str = None, contents: Contents = None, uid: str = '123', is_show_content: bool = False):
        while True:
            if question:
                sid, contents = self.chat(question, contents=contents, uid=uid, is_show_content=is_show_content)

            question = input("\n>>>>>>Ask: ")
            if not question:
                continue
            if question == 'exit':
                break
            
        return contents
        
