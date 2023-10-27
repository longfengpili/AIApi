# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-10-26 13:39:12
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-10-27 11:46:02
# @github: https://github.com/longfengpili

import re

from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import (  # type: ignore
    Magics,
    line_cell_magic,
    line_magic,
    cell_magic,
    magics_class,
)
from IPython.core.magic_arguments import (  # type: ignore
    argument,
    magic_arguments,
    parse_argstring,
)

from .config import AIConfig
from .chat import XinghuoChat
from .contents import Content, Contents


@magics_class
class XhChater(Magics):

    def __init__(self, shell: InteractiveShell = None):
        super(XhChater, self).__init__(shell)

    def xhchat(self, ainame: str = 'xinghuo'):
        aiconf = AIConfig.load(ainame)
        if not aiconf:
            aiid = input('please input your appid:')
            aikey = input('please input your appikey:')
            aisecret = input('please input your appsecret:')
            aiconf = AIConfig(ainame, aiid, aikey, aisecret)
            aiconf.dump()

        xhchat = XinghuoChat(ainame, aiconf.appid, aiconf.appkey, aiconf.appsecret)
        return xhchat

    def _concat_inputs(self, *inputs: tuple):
        inputs = [text.strip() for text in inputs if text.strip()]
        content = '\n'.join(inputs)
        content = Content(**{'role': 'user', 'content': content})
        contents = Contents(content)
        return contents

    def _convert_to_code(self, content: str):
        def convert_non_code(content: str, c_start: int, c_end: int = None):
            non_code = content[c_start:c_end] if c_end else content[c_start:]
            non_code = [f'# {s}' for s in non_code.split('\n') if s.strip() and not s.startswith('```')]
            non_code = '\n'.join(non_code)
            return non_code

        all_code_spans = []
        reg = r"`{3}([\w]*)\n([\S\s]+?)\n`{3}"
        for i in re.finditer(reg, content):
            all_code_spans.append(i.span(2))

        if len(all_code_spans) == 0:
            all_code_spans.append((0, len(content)))

        c_pos = 0
        convert_code = []
        for c_start, c_end in all_code_spans:
            non_code = convert_non_code(content, c_pos, c_start)
            code = content[c_start:c_end].strip()
            convert_code.extend([non_code, code])
            c_pos = c_end

        last_non_code = convert_non_code(content, c_pos)
        convert_code.append(last_non_code)

        return '\n'.join(convert_code)

    @line_magic
    def chat_single(self, line):
        xhchat = self.xhchat()
        contents = self._concat_inputs(line)
        sid, contents = xhchat.chat(contents)
        execution_id = self.shell.execution_count
        code = self._convert_to_code(contents.last_content)
        program_out = f"# Assistant Code for Cell [{execution_id}]:\n{code}"
        self.shell.set_next_input(program_out)

    @magic_arguments()
    @argument('--verobse', '-v', action="store_true", help="Whether to show ask")
    @argument('--save', '-s', action="store_true", help="Whether to save history")
    @cell_magic
    def chat(self, line, cell=None):
        args = parse_argstring(self.chat, line)
        is_show_content = True if args.verobse else False
        is_save = True if args.save else False
        contents = self._concat_inputs(cell)
        print(f'>>>>>>Ask:{contents.last_content}\n')
        xhchat = self.xhchat()
        contents = xhchat.chat_stream(contents, is_show_content=is_show_content)
        if is_save:
            contents.dump(xhchat.appname)


# 注册magic命令
def load_ipython_extension(ipython):
    ipython.register_magics(XhChater)

# #  注册魔术命令
# get_ipython().register_magics(XhChater)
