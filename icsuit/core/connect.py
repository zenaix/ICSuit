# -*- coding:utf-8 -*-

import sys
import socket
import threading
import multiprocessing

class Connect(threading.Thread):
    def __init__(self, name, seed=None, timeout=10, probe=None, target=None):
        super(Connect, self).__init__(name=name)
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        except socket.error, msg:
            print "Create socket failed, error code[%s], %s" % (str(msg[0]), msg[1])
            sys.exit(1)

    def set_seed(self, seed):
        if isinstance(seed, int):
            self.seed = seed
            return True
        return False

    def set_timeout(self, timeout):
        if isinstance(timeout, int):
            self.timeout = timeout
            return True
        return False

    def set_probe(self, probe):
        if probe is None:
            return False
        else:
            self.probe = probe
            return True

    def set_target(self, target):
        if target is None:
            return False
        else:
            self.target = target
            return True
            
def scan(module_path, option):
    module = importmod(module_path)

    if module.scanner == "connect":
        d = multiprocessing.Manager().dict()
        for key in option:
            d[key] = option[key]

        p = multiprocessing.Process(target=module.start, args=(d, ))
        p.daemon = True

        p.start()
        p.join()

        return True
    else:
        return False
