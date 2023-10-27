# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-09-08 14:22:39
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-10-27 11:22:20
# @github: https://github.com/longfengpili


# 注册magic命令, 在jupyter中使用`%load_ext xinghuo`加载
def load_ipython_extension(ipython):
    ipython.register_magics(XhChater)

