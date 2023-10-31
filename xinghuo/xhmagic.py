# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-10-26 13:39:12
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-10-31 19:14:57
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

from traitlets import Bool, Dict, Instance, Unicode, default, observe  # noqa
from traitlets.config.loader import Config


@magics_class
class XhChater(Magics):
    ainame = Unicode('ainame', help='ainame').tag(config=True)

    def __init__(self, shell: InteractiveShell = None):
        super(XhChater, self).__init__(shell)
        self.ainame = 'xinghuo'

    @property
    def xhchat(self):
        aiconf = AIConfig.load(self.ainame)
        if not aiconf:
            aiid = input('please input your appid:')
            aikey = input('please input your appikey:')
            aisecret = input('please input your appsecret:')
            aiconf = AIConfig(self.ainame, aiid, aikey, aisecret)
            aiconf.dump()

        xhchat = XinghuoChat(aiconf.appname, aiconf.appid, aiconf.appkey, aiconf.appsecret)
        return xhchat

    def _convert_to_code(self, content: str):
        def convert_non_code(content: str, c_start: int, c_end: int = None):
            non_code = content[c_start:c_end] if c_end is not None else content[c_start:]
            non_code = [f'# {s.strip()}' for s in non_code.split('\n') if s.strip() and not s.startswith('```')]
            non_code = '\n'.join(non_code)
            return non_code

        all_code_spans = []
        reg = r"`{3}([\w]+)\n([\S\s]+?)\n`{3}"
        for i in re.finditer(reg, content):
            all_code_spans.append(i.span(2))

        c_pos = 0
        convert_codes = []
        if all_code_spans:
            for c_start, c_end in all_code_spans:
                non_code = convert_non_code(content, c_pos, c_start)
                code = content[c_start:c_end].strip()
                convert_codes.extend([non_code, code])
                c_pos = c_end

        last_non_code = convert_non_code(content, c_pos)
        convert_codes.append(last_non_code)

        return '\n'.join([code for code in convert_codes if code])

    def chat_jupyter(self, answer: str, number: int = 4, is_show_content: bool = True):
        xhchat = self.xhchat
        contents = self.shell.user_ns.get('CONTENTS', Contents())
        s_contents = contents[-number:]
        sid, r_contents = xhchat.chat(answer, s_contents, is_show_content=is_show_content)
        # 新内容传递给user_ns
        contents.extend(r_contents[-2:])
        self.shell.user_ns['CONTENTS'] = contents
        return contents

    def chat_input(self, contents):
        # 输出结果
        execution_id = self.shell.execution_count
        code = self._convert_to_code(contents.last_content)
        program_out = f"# Assistant Code for Cell [{execution_id}]:\n{code}"
        print('>>>>>>>>>>>>Result:\n')
        self.shell.run_cell(program_out)

        # input to shell cell
        self.shell.set_next_input(program_out)

    @magic_arguments()
    @argument('--verobse', '-v', action="store_true", help="Whether to show ask")
    @argument('--save', '-s', action="store_true", help="Whether to save history")
    @argument('--input', action="store_true", help="Whether to save history")
    @argument('--number', '-n', default=6, type=int, help="how many contents to ai")
    @line_cell_magic
    def chat(self, line, cell=None):
        '''[summary]
        
        [chat in jupyter]
        
        Args:
            line ([str]): [line]
            cell ([str]): [cell] (default: `None`)
        '''
        if not cell:
            contents = self.chat_jupyter(line)
            return

        args = parse_argstring(self.chat, line)
        is_show_content = True if args.verobse else False
        number = args.number
        contents = self.chat_jupyter(cell, number=number, is_show_content=is_show_content)

        is_save = True if args.save else False
        if is_save:
            contents.dump(self.ainame)

        isinput = args.input
        if isinput:
            self.chat_input(contents)

    @line_magic
    def aiconfig(self, line):
        """Used for displaying and modifying xinghuo configurations.

        Exemplar usage:

        - %xhconfig
          print all the configurable parameters and its current value

        - %xhconfig <parameter_name>
          print the current value of the parameter

        - %xhconfig <parameter_name>=<value>
          set the value of the parameter
        """
        line = line.strip().split('#')[0].strip()
        all_class_configs = self.class_own_traits()

        if not line or line.startswith('#'):
            doc = self.class_get_help()
            print(doc)
            return
        elif line in all_class_configs.keys():
            return getattr(self, line)
        elif '=' in line:
            param, value = line.split('=')
            param, value = param.strip(), value.strip()
            if param in all_class_configs.keys():
                cfg = Config()
                exec(f'cfg.{self.__class__.__name__}.{line}', self.shell.user_ns, locals())
                self.update_config(cfg)
        else:
            pass


# 注册magic命令(如果使用mymagics.py, 则下边的函数不重要)
def load_ipython_extension(ipython):
    ipython.register_magics(XhChater)

# #  注册魔术命令
# get_ipython().register_magics(XhChater)
