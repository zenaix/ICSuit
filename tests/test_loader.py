# -*- coding: utf-8 -*-

import os
import unittest

from context import icsuit

from icsuit.cli.loader import findmod, importmod, listmod

class TestLoader(unittest.TestCase):
    """Unit test cases for cli.loader."""

    def test_listmod(self):
        os.chdir('..')
        print
        print listmod()
        os.chdir('tests')
 
    def test_findmod(self):
        os.chdir('..')
        print findmod('probe/nostate/tcpsyn')
        print findmod('probe/nostates/tcpsyn')
        os.chdir('tests')

    def test_importmod(self):
        os.chdir('..')
        module = importmod('probe/nostate/tcpsyn')
        option = getattr(module, 'option')
        print
        print option
        os.chdir('tests')

if __name__ == '__main__':
    unittest.main()
