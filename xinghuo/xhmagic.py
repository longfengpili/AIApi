# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-10-26 13:39:12
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-02 16:03:28
# @github: https://github.com/longfengpili

import re

from IPython.core.error import UsageError
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

from .chat import XinghuoChat
from .contents import Content, Contents

from traitlets import Bool, Dict, Instance, Unicode, default, observe  # noqa
from traitlets.config.loader import Config


@magics_class
class XinghuoMagics(Magics):
    appname = Unicode('xinghuo', 
                      help=('current use appname, default: xinghuo ~')
                      ).tag(config=True)
    appid = Unicode(allow_none=True, 
                    help=('current use appid')
                    ).tag(config=True)
    apikey = Unicode(allow_none=True, 
                     help=('current use apikey')
                     ).tag(config=True)
    apisecret = Unicode(allow_none=True, 
                        help=('current use apisecret')
                        ).tag(config=True)

    def __init__(self, shell: InteractiveShell = None):
        super(XinghuoMagics, self).__init__(shell)

    @property
    def xhchat(self):
        if not all([self.appname, self.appid, self.apikey, self.apisecret]):
            self.appid = input('please input your appid:')
            self.apikey = input('please input your apikey:')
            self.apisecret = input('please input your apisecret:')

        xhchat = XinghuoChat(self.appname, self.appid, self.apikey, self.apisecret)
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
        try:
            sid, r_contents = xhchat.chat(answer, s_contents, is_show_content=is_show_content)
        except Exception as e:
            raise e
        # 新内容传递给user_ns
        contents.extend(r_contents[-2:])
        self.shell.user_ns['CONTENTS'] = contents
        return contents

    def chat_input(self, contents):
        # 输出结果
        execution_id = self.shell.execution_count
        code = self._convert_to_code(contents.last_content)
        program_out = f"# Assistant Code for Cell [{execution_id}]:\n{code}"
        # print('>>>>>>>>>>>>Result:\n')
        # self.shell.run_cell(program_out)

        # input to shell cell
        self.shell.set_next_input(program_out)

    @magic_arguments()
    @argument('--verobse', '-v', action="store_true", help="Whether to show ask")
    @argument('--save', '-s', action="store_true", help="Whether to save history")
    @argument('--input', '-i', action="store_true", help="Whether to save history")
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
            contents.dump(self.appname)

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
        class_configs = self.class_own_traits()

        if not line or line.startswith('#'):
            doc = self.class_get_help()
            print(doc)
            return
        elif line.lower() in class_configs.keys():
            return getattr(self, line.lower())
        elif '=' in line and line.split('=')[0].strip().lower() in class_configs.keys():
            param, value = line.strip().split('=')
            line = param.lower() + '=' + value
            cfg = Config()
            exec(f'cfg.{self.__class__.__name__}.{line}', self.shell.user_ns, locals())
            self.update_config(cfg)
        elif line in ('-h', '--help'):
            print(
                    "It supports the following usage:\n"
                    "- %aiconfig\n  print all the configurable parameters and its current value\n"
                    "- %aiconfig <parameter_name>\n  print the current value of the parameter\n"
                    "- %aiconfig <parameter_name>=<value>\n  set the value of the parameter"
                )
        else:
            raise UsageError(
                    f"Invalid usage of the aiconfig command: {line}.\n"
                    f"It only supports the following params: {class_configs.keys()}"
                )


# 注册magic命令(如果使用mymagics.py, 则下边的函数不重要)
def load_ipython_extension(ipython):
    ipython.register_magics(XinghuoMagics)

# #  注册魔术命令
# get_ipython().register_magics(XhChater)
