# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:29:34
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-19 11:38:38
# @github: https://github.com/longfengpili


import json
import ssl
import websocket

from .auth import XingHuoAuth
from .contents import Content, Contents


class XinghuoChat(XingHuoAuth):

    def __init__(self, appid: str, apikey: str, apisecret: str, sparkurl: str):
        self.appid = appid
        self.domain = 'generalv2'
        self.sid = ''
        self.answer = ''
        self.contents = Contents()
        super(XinghuoChat, self).__init__(apikey, apisecret, sparkurl)

    @property
    def connection(self):
        connection = websocket.create_connection(self.auth_url)
        return connection

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
            self.connection.close()
            raise ValueError(f'请求错误: {code}, {data}')

        if sid != self.sid:
            self.sid = sid
            self.answer = ''

        choices = data['payload']['choices']
        status = choices['status']
        content = choices['text'][0]['content']
        print(content, end='')
        self.answer += content
        if status == 2:
            usage = data['payload']['usage']['text']
            # self.connection.close()

        return sid, status, usage

    def chat(self, contents: Contents, uid: str = '123', issave: bool = True, savefile: str = 'test.csv'):
        print(contents)
        print("\n>>>>>>Answer:")

        connection = self.connection
        message = self.build_message(contents)
        connection.send(message)
        while response := connection.recv():
            sid, status, usage = self.parse_response(response)

        answer = Content('assistant', self.answer, sid=sid, **usage)
        contents.append(answer)
        
        if issave:
            contents.dump(savefile)

        return sid, contents

    def chat_stream(self, contents: Contents = None, savefile: str = 'test.csv'):
        if not contents:
            contents = Contents()

        while True:
            if contents.last_role == 'user':
                sid, contents = self.chat(contents, issave=False)

            query = input("\n\n>>>>>>Ask: ")
            if not query:
                continue
            if query == 'exit':
                contents.dump(savefile)
                break

            question = Content('user', query)
            contents.append(question)
            
        
