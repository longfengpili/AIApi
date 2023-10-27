# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-10-27 11:15:46
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-10-27 11:16:34
# @github: https://github.com/longfengpili


from xinghuo.xhmagic import XhChater


c = get_ipython()

# #  注册魔术命令
c.register_magics(XhChater)
