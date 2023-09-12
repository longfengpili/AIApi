# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:44:15
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-12 11:15:08
# @github: https://github.com/longfengpili

from conf import APPID, APIKEY, APISECRET
from xinghuo.ws_param import WsParam
from xinghuo.ws_app import WsApp


if __name__ == "__main__":
    appid = APPID
    apikey = APIKEY
    apisecret = APISECRET
    sparkurl = 'wss://spark-api.xf-yun.com/v2.1/chat'
    wsparam = WsParam(apikey, apisecret, sparkurl)
    wsurl = wsparam.create_url()

    question = [{'role': 'user', 'content': '介绍下pandas'}]
    wsapp = WsApp(wsurl)
    wsapp.main(appid, question)
