# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-10-27 11:15:46
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-01 18:46:47
# @github: https://github.com/longfengpili


from xinghuo.xhmagic import XinghuoMagics


c = get_ipython()

# #  注册魔术命令
c.register_magics(XinghuoMagics)
