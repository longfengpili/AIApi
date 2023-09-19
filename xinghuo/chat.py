# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:29:34
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-19 10:23:07
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
            # usage = data['payload']['usage']
            # print(usage)
            self.connection.close()
        return sid, status

    def chat(self, contents: Contents, uid: str = '123'):
        connection = self.connection
        message = self.build_message(contents)
        connection.send(message)
        
        while response := connection.recv():
            sid, status = self.parse_response(response)
            # response = connection.recv()

        answer = Content('assistant', self.answer, sid=sid)
        contents.append(answer)
        return sid, contents

    def chat_stream(self):
        contents = Contents()
        while True:
            query = input("\n\n>>>>>>Ask: ")
            if not query:
                continue
            if query == 'exit':
                break

            question = Content('user', query)
            contents.append(question)
            print(contents)
            sid, contents = self.chat(contents)
            print(sid)

    def save_data(self, contents: Contents, answer: str):
        answer = Content('assistant', answer)
        contents.append(answer)
        contents.dump('test.csv')
