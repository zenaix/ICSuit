# -*- coding:utf-8 -*-

from icsuit.cli import CLI
from icsuit.core.nostate import scan

class ICSCLI(CLI):
    def __init__(self):
        CLI.__init__(self)

    def do_run(self, line):
        """Usage:
        run, run the selected module.
        """
        scan(self._module_path, self._option)
    
    def do_db_status(self, line):
        """Usage:
        db_status, show the current database status
        """
        pass

if __name__ == "__main__":
    cli = ICSCLI()
    cli.cliloop()
