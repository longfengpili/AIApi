# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-11 18:21:36
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-10-30 19:36:10
# @github: https://github.com/longfengpili


from xinghuo.contents import Content, Contents


class TestModel:

    def setup_method(self, method):
        self.m1 = Content('user', 'message q1')
        self.m2 = Content('assistant', 'message a1')
        self.m3 = Content.load('{"role": "user", "content": "content1"}')

    def teardown_method(self, method):
        pass

    def test_content(self):
        print(self.m1, self.m2, self.m3)

    def test_contents(self):
        ms = Contents(self.m1, self.m2, self.m3)
        print(ms)
        print(ms.data)

    def test_contents_index(self):
        ms = Contents(self.m1, self.m2, self.m3)
        print(ms[1])
        print(ms[-1:])
        print(ms[-2:])

    def test_dump(self):
        ms = Contents(self.m1, self.m2, self.m3)
        ms.dump('./test.csv')

    def test_load(self):
        ms = Contents.load('./test.csv')
        print(ms)
