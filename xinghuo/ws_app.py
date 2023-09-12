# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:29:34
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-12 10:38:34
# @github: https://github.com/longfengpili


import json
import ssl
import websocket

import _thread as thread

from messages import Message, Messages


class WsApp:

    def __init__(self, wsurl: str):
        self.wsurl = wsurl
        self.domain = 'generalv2'

    @property
    def app(self):
        app = websocket.WebSocketApp(self.wsurl)
        app.domain = self.domain
        app.on_open = self.on_open
        app.on_close = self.on_close
        app.on_error = self.on_error
        app.on_message = self.on_message
        return app

    def get_params(self, appid: str, question: list[dict]):
        data = {
            "header": {
                "app_id": appid,
                "uid": "1234"
            },
            "parameter": {
                "chat": {
                    "domain": self.domain,
                    "random_threshold": 0.5,
                    "max_tokens": 2048,
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": question
                }
            }
        }
        return data

    def run(self, ws, *args):
        appid, question = ws.appid, ws.question
        params = self.get_params(appid, question)
        data = json.dumps(params)
        ws.send(data)

    def on_open(self, ws):
        thread.start_new_thread(self.run, (ws,))

    def on_close(self, ws):
        print('close')

    def on_error(self, ws, error):
        print(error)

    def on_message(self, ws, message):
        # print(f"\n=={message}")
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            print(f'请求错误: {code}, {data}')
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            print(content, end='')
            global answer
            answer += content
            # print(1)
            if status == 2:
                ws.close()

    def main(self, appid: str, question: list):
        websocket.enableTrace(False)
        ws = self.app
        ws.appid = appid
        ws.question = question
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
