# -*- coding:utf-8 -*-

import os
import sys
import string

from icsuit.core import conf
from icsuit.core.loader import listmod, importmod
from icsuit.lib.util.output import column_print

class CLI(object):

    identchars = string.ascii_letters + string.digits + '_'
    welcome = "Welcome to icsuit.\nVersion: v0.1\n"
    doc_header = "Type 'help [command]' for more information."
    no_help = "No help information for '%s'."

    def __init__(self, complete_key='tab', prompt='icsuit>'):
        self.complete_key = complete_key
        self.prompt = prompt
        
        self.stdin = sys.stdin
        self.stdout = sys.stdout

    def cliloop(self, welcome=None):
        self.preloop()

        # 设置自动补全
        if not self.complete_key:
            self.complete_key = "tab"

        import readline
        readline.set_completer(self.complete)
        readline.parse_and_bind(self.complete_key+": complete")

        if welcome is not None:
            self.welcome = welcome
        if self.welcome:
            self.stdout.write(str(self.welcome)+"\n")

        # 命令循环
        stop = None   
        while not stop:
            try:
                line = raw_input(self.prompt)
            except EOFError:
                line = 'EOF'

            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)

        self.postloop()

    def preloop(self):
        """命令循环开始前执行初始化，仅执行一次
        """
        self._option = None
        self._module_path = None

    def precmd(self, line):
        """对命令进行解释之前做预处理
        """
        return line

    def parseline(self, line):
        line = line.strip()
        if not line:
            return None, None, line
        # 设置'?'为help命令的别名
        elif line[0] == '?':
            line = 'help ' + line[1:]

        # 解析输入，分离命令和参数
        i, n = 0, len(line)
        while i < n and line[i] in self.identchars: i += 1
        cmd, arg = line[:i], line[i:].strip()

        return cmd, arg, line

    def onecmd(self, line):
        cmd, arg, line = self.parseline(line)
        # 处理无效输入与空命令
        if not line or cmd is None or cmd == '':
            return self.emptyline()
        else:
            if line == 'EOF':
                self.lastcmd = ''
            else:
                self.lastcmd = line

            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                # 非内置命令将被当作shell脚本执行
                return self.default(line)

            return func(arg)

    def postcmd(self, stop, line):
        """每次命令循环最后执行的函数，返回结果为真时结束命令循环，可在该函数中进行命令的后期处理
        """
        return stop

    def postloop(self):
        """CLI结束前最后执行的函数，该函数被设计用来完成所有清理工作
        """
        pass
                
    def get_names(self):
        return dir(self.__class__)

    def completedefault(self, *ignore):
        return []

    def completenames(self, text, *ignored):
        dotext = 'do_' + text
        return [a[3:] for a in self.get_names() if a.startswith(dotext)]

    def complete(self, text, state):
        if state == 0:
            import readline
            line_buf = readline.get_line_buffer()
            line = line_buf.lstrip()
            strip_len = len(line_buf) - len(line)
            begidx = readline.get_begidx() - strip_len
            endidx = readline.get_endidx() - strip_len

            if begidx > 0:
                cmd, arg, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    def emptyline(self):
        """忽略为空的命令
        """
        pass

    def default(self, line):
        """将未定义的命令作为shell命令执行
        """
        try:
            os.system(line)
        except Exception, e:
            print e

    ##############################内置命令##############################

    def do_help(self, arg):
        """Usage:
        help [command], see all supported commands or  help infomation of specified command.

        alias: '?'
        """
        if arg:
            try:
                doc = getattr(self, 'do_' + arg).__doc__
                if doc:
                    self.stdout.write("%s\n" % str(doc))
                    return
            except AttributeError:
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
        else:
            names = self.get_names()
            names.sort()

            cmds = []
            cmds_doc = []
            db_cmds = []
            db_cmds_doc = []

            for name in names:
                if name[:3] == 'do_':
                    cmd = name[3:]
                    if cmd[:3] == 'db_':
                        db_cmds.append(cmd)
                        db_cmds_doc.append(getattr(self, name).__doc__.split('\n')[1].split(',')[1][1:])
                    else:
                        cmds.append(cmd)
                        cmds_doc.append(getattr(self, name).__doc__.split('\n')[1].split(',')[1][1:])

            self.stdout.write("%s\n\n" % self.doc_header)
            column_print(tab=False, ruler='=', Command=cmds, Description=cmds_doc)
            self.stdout.write("\n")
            column_print(tab=False, ruler='=', Database_Command=db_cmds, Description=db_cmds_doc)
                    
    def complete_help(self, *args):
        return self.completenames(*args)

    def do_show(self, arg):
        """Usage:
        show [module name], show supported modules or options of chosen module.
        """
        if arg == "options":
            if self._option is None:
                print "Please choose a module first, type 'help use' for more information."
            else:
                name = []
                value = []
                for key in self._option:
                    name.append(key)
                    value.append(str(self._option[key]))
                column_print(Option_Name=name, Current_Setting=value)
        elif arg == "":
            # 获取最新的模块列表
            module_group = listmod()
            info = []
            for module_name in module_group:
                if module_name in conf.module:
                    info.append(conf.module[module_name])
                else:
                    info.append("Need register.")
                
            column_print(Supported_Module=module_group, Description=info)
        else:
            print "Syntax error, type 'help show' for more information."

    def complete_show(self, text, *ignore):
        if 'options'.startswith(text):
            return ['options']
        else:
            return []

    def do_use(self, arg):
        """Usage:
        use [module name], choose a module to use.
        """
        if self._module_path is not None:
            print "Please exit the current context first."
            return

        module = importmod(arg)
        if module is None:
            print "Import module '%s' failed, please check if the module name is right." % arg
        else:
            self._option = module.option
            self._module_path = arg
            self.prompt = "icsuit("+self._module_path.split('/')[-1]+")> "

    def complete_use(self, text, line, begidx, *ignore):
        module_group = listmod()

        return [a[begidx-4:] for a in module_group if a.startswith(line[4:])]

    def do_exit(self, arg):
        """Usage:
        exit, exit the module context or exits from the cli.
        """
        if self._module_path is None:
            return -1
        else:
            self._module_path = None
            self._option = None
            self.prompt = "icsuit> "

    def do_set(self, arg):
        """Usage:
        set [option name][option value], set value for the specified option.
        """
        if self._option is None:
            print "Please choose a module first, type 'help use' for more information."
            return

        data = arg.split(' ')
        if len(data) != 2:
            print "Syntax error."
            print getattr(self, 'do_set').__doc__
        else:
            try:
                self._option[data[0]] = data[1]
            except KeyError:
                print "Unknown option given, please use 'show option' for more information."

    def complete_set(self, text, line, begidx, *ignore):
        if self._option is None:
            return []

        l = []
        for key in self._option:
            l.append(key)
        return [a[begidx-4:] for a in l if a.startswith(text)]
            
if __name__ == "__main__":
    cli = CLI()
    cli.cliloop()
