# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-11 14:48:03
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-19 11:14:19
# @github: https://github.com/longfengpili


import json


class Content:

    def __init__(self, role: str, content: str, **kwargs):
        self.role = role
        self.content = content
        self.kwargs = kwargs

    def __repr__(self):
        return self._repr

    def __getattr__(self, name: str):
        return self.kwargs.get(name)

    @property
    def _repr(self):
        content = self.content.split('\n')[0]
        sid = self.sid
        _repr = f"[{self.role}]{content[:20]}..."
        _repr = f"{_repr}({sid})" if sid else _repr
        return _repr

    @property
    def data(self):
        data = {
            'role': self.role,
            'content': self.content,
            'kwargs': self.kwargs
        }
        data = json.dumps(data, ensure_ascii=False)
        return data

    @property
    def chatdata(self):
        data = {
            'role': self.role,
            'content': self.content
        }
        return data

    @classmethod
    def load(cls, data: str):
        data = json.loads(data)
        if data:
            return cls(**data)


class Contents:

    def __init__(self, *contents: list[Content, ...]):
        self.contents = contents

    def __repr__(self):
        contents = [content._repr for content in self.contents]
        divider_line = '=' * 50
        contents = [divider_line, *contents, divider_line]
        contents = '\n'.join(contents)
        return contents

    def append(self, content: Content):
        contents = list(self.contents)
        contents.append(content)
        self.contents = contents
        return self

    @property
    def last_role(self):
        last_content = self.contents[-1]
        last_role = last_content.role
        return last_role

    @property
    def data(self):
        contents = [content.data for content in self.contents]
        data = '\n'.join(contents) + '\n'
        return data

    @property
    def chatdata(self):
        contents = [content.chatdata for content in self.contents]
        return contents

    def dump(self, filename: str):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(self.data)

    @classmethod
    def load(cls, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            contents = [Content.load(line) for line in lines]
            return cls(*contents)