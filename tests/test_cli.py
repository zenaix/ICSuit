# -*- coding: utf-8 -*-

import os
import unittest

from context import icsuit

from icsuit.cli.core import CLI

class TestLoader(unittest.TestCase):
    """Unit test cases for cli.core."""

    def test_cli(self):
        os.chdir('..')
        cli = CLI()
        cli.cliloop()
        os.chdir('tests')
 
if __name__ == '__main__':
    unittest.main()
