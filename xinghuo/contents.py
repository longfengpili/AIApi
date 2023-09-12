# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-11 14:48:03
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-12 10:53:23
# @github: https://github.com/longfengpili


import json


class Content:

    def __init__(self, role: str, content: str, **kwargs):
        self.role = role
        self.content = content
        self.kwargs = kwargs

    def __repr__(self):
        return f"[{self.role}]{self.content}"

    @property
    def data(self):
        data = {
            'role': self.role,
            'content': self.content,
            'kwargs': self.kwargs
        }
        data = json.dumps(data)
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
        return f"{self.contents}"

    def append(self, content: Content):
        contents = list(self.contents)
        contents.append(content)
        return Contents(*contents)

    @property
    def data(self):
        contents = [content.data for content in self.contents]
        data = '\n'.join(contents) + '\n'
        return data

    def dump(self, filename: str):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(self.data)

    @classmethod
    def load(cls, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            contents = [Content.load(line) for line in lines]
            return cls(*contents)
