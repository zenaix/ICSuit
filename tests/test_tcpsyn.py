# -*- coding: utf-8 -*-

import os
import sys
import time
import threading

from context import icsuit
from icsuit.module.probe.nostate import tcpsyn


class Tester(object):
    def __init__(self):
        pass

    def test_tcpsyn1(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "1"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/27"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn5(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "5"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/27"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn9(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "9"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/24"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn10(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "10"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/24"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn50(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "50"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/24"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn90(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "90"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/20"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn100(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "100"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/20"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn500(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "500"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/20"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn900(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "900"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/16"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')
        
    def test_tcpsyn1000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "1000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/16"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn5000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "5000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/16"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn9000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "9000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/14"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn10000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "10000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/14"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn20000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "20000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/14"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn49000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "49000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/13"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn50000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "50000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/13"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn75000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "75000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/11"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn99000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "99000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/11"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn100000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "100000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/11"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn150000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "150000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/11"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def test_tcpsyn200000(self):
        os.chdir('..')
        t = time.time()
        tcpsyn.option["BANDWIDTH"] = "200000"
        tcpsyn.option["TARGET_IP"] = "10.13.22.196/11"
        tcpsyn.start(None, tcpsyn.option)
        os.chdir('tests')

    def run(self):
        lock = threading.Lock()

        self.test_tcpsyn1()
        self.test_tcpsyn5()
        self.test_tcpsyn9()
        self.test_tcpsyn10()
        self.test_tcpsyn50()
        self.test_tcpsyn90()
        self.test_tcpsyn100()
        self.test_tcpsyn500()
        self.test_tcpsyn900()
        self.test_tcpsyn1000()
        self.test_tcpsyn5000()
        self.test_tcpsyn9000()
        self.test_tcpsyn10000()
        self.test_tcpsyn20000()
        self.test_tcpsyn49000()
        self.test_tcpsyn50000()
        self.test_tcpsyn75000()
        self.test_tcpsyn99000()
        self.test_tcpsyn100000()
        self.test_tcpsyn150000()
        self.test_tcpsyn200000()

if __name__ == '__main__':
    Tester().run()
