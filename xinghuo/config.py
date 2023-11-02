# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-10-27 09:26:20
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-02 11:48:19
# @github: https://github.com/longfengpili


import json
from pathlib import Path


class AIConfig:

    dumppath = Path(Path.home(), '.mysettings')

    def __init__(self, appname, appid, apikey, apisecret, **kwargs):
        self.appname = appname
        self.appid = appid
        self.apikey = apikey
        self.apisecret = apisecret
        self.kwargs = kwargs

    def __getattr__(self, item: str):
        return self.kwargs.get(item)

    def __getattribute__(self, item: str):
        return super(AIConfig, self).__getattribute__(item)

    def __repr__(self):
        return f"{self.appname}({self.appid})"

    @property
    def data(self):
        data = {'appname': self.appname, 
                'appid': self.appid,
                'apikey': self.apikey,
                'apisecret': self.apisecret}
        data.update(self.kwargs)
        return data

    @property
    def data_json(self):
        data = json.dumps(self.data)
        return data

    @classmethod
    def load_from_json(cls, jsondata: str):
        kwargs = json.loads(jsondata)
        return cls(**kwargs)

    @classmethod
    def load(cls, appname: str):
        print(appname)
        dumpfile = Path(cls.dumppath, f'{appname}.json')
        if not dumpfile.exists():
            return

        with dumpfile.open('r', encoding='utf-8') as f:
            data = json.load(f)

        return cls(**data)

    def dump(self):
        dumppath = self.dumppath
        dumpfile = Path(dumppath, f'{self.appname}.json')
        print(dumpfile)

        if not dumppath.exists():
            dumppath.mkdir()

        with dumpfile.open('w', encoding='utf-8') as f:
            json.dump(self.data, f)
        return dumpfile

    def get(self, item: str):
        try:
            return self[item]
        except:
            return self.kwargs.get(item)
