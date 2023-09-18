# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:23:57
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-18 11:07:27
# @github: https://github.com/longfengpili

import hmac
import base64
import hashlib

from time import mktime
from datetime import datetime
from wsgiref.handlers import format_date_time

from urllib.parse import urlparse
from urllib.parse import urlencode


class XingHuoAuth:

    def __init__(self, apikey: str, apisecret: str, sparkurl: str):
        self.apikey = apikey
        self.apisecret = apisecret
        self.host = urlparse(sparkurl).netloc
        self.path = urlparse(sparkurl).path
        self.sparkurl = sparkurl

    @property
    def auth_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.apisecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.apikey}", algorithm="hmac-sha256", \
                                 headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.sparkurl + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url
