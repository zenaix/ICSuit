# -*- coding:utf-8 -*-

import pdb

import sys
import time
import socket
import threading
import multiprocessing

from icsuit.core.loader import importmod
from icsuit.core.cyclic import iprange, ipcycle, ipmin, ipmax, ipmask
from icsuit.lib.util.output import timeformat

scan_stop = False

class Sender(threading.Thread):
    def __init__(self, lock, name, seed=None, rate=50, timeout=1, probe=None, target=None):
        super(Sender, self).__init__(name=name)
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        except socket.error, msg:
            print "Create socket failed, error code[%s], %s" % (str(msg[0]), msg[1])
            sys.exit(1)

        self.lock = lock
        self.seed = seed
        self.rate = rate
        self.probe = probe
        self.count = 0
        self.target = target
        self.timeout = timeout
    
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

    def set_rate(self, rate):
        if isinstance(rate, int) and rate > 0:
            self.rate = rate
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

    def presend(self):
        status, ip_range = iprange(self.target[0])
        total = 2**ipmask(ip_range)
        self.start = time.time()
        self.begin = time.time()

        return (status, ip_range, total)

    def bandwidth(self, ip):
        if self.rate < 20:
            time.sleep(round(1.0/self.rate, 1))
            self.send(ip, self.target[1])
        elif self.rate < 220:
            if self.count % self.rate == 0:
                wait = time.time()-self.start
                wait = round(1.0-wait, 2)
                time.sleep(wait)
                self.start = time.time()
            self.send(ip, self.target[1])
        elif self.rate < 2200:
            n  = int(self.rate/275)
            if self.count % self.rate == 0:
                wait = time.time()-self.start
                wait = round(1.0-n*0.01-wait, 2)
                if wait <= 0:
                    time.sleep(0.01)
                else:
                    time.sleep(wait)
                self.start = time.time()
            self.send(ip, self.target[1])
        elif self.rate < 6600:
            n  = int(self.rate/550)
            if self.count % self.rate == 0:
                wait = time.time()-self.start
                wait = round(1.0-n*0.01-wait, 2)
                if wait <= 0:
                    pass
                else:
                    time.sleep(wait)
                self.start = time.time()
            self.send(ip, self.target[1])
        elif self.rate < 11100:
            n  = int(self.rate/1100)
            if self.count % self.rate == 0:
                wait = time.time()-self.start
                wait = round(1.0-n*0.01-wait, 2)
                if wait <= 0:
                    pass
                else:
                    time.sleep(wait)
                self.start = time.time()
                #sys.stdout.write("%f, %s\n" % (wait, str(self.start)))
            self.send(ip, self.target[1])
        else:
            if self.count % 9250 == 0:
                time.sleep(0.01)
            self.send(ip, self.target[1])

    def send(self, ip, port):
        pass

    def bar(self, total):
        if total > 10000 or total > 5*self.rate:
            if ((self.count % (total/1000 + 1)) == 0) or self.count % self.rate == 0 or self.count == total:
                percent = int(100*self.count/total)
                timecost = time.time()-self.begin
                sys.stdout.write("Processing %d%%[%s], Packts: %s, Rate: %dp/s, Rest time: %s        \r" % (percent, int(percent*0.8)*"#", self.count, round(float(self.count)/(timecost)), timeformat(int((total-self.count)*timecost/self.count))))
                sys.stdout.flush()

    def sendloop(self):
        global scan_stop
        status, ip_range, total = self.presend()

        if ip_range is None:
            print "Syntax error!"
            return status
        elif status:
            #sys.stdout.write("%s\n" % str(self.start))
            for ip in ipcycle(ip_range, seed=self.seed):
                try:
                    self.bandwidth(ip)
                except socket.error:
                    self.sock.close()
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

                # 数据包计数器
                self.count += 1
                # 进度条
                self.bar(total)
        else:
            try:
                self.send(self.target[0], self.target[1])
            except socket.error:
                scan_stop = True

        timeout = 0.05 
        while not scan_stop:
            if timeout > self.timeout:
                scan_stop = True
                break
            else:
                time.sleep(timeout)
                timeout *= 2

        self.postsend(scan_stop)

    def postsend(self, status):
        return status

    def run(self):
        self.sendloop()

class Recver(threading.Thread):
    def __init__(self, lock, name, target=None):
        super(Recver, self).__init__(name=name)
        try:
            self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x03))
        except socket.error, msg:
            print "Create socket failed, error code[%s], %s" % (str(msg[0]), msg[1])
            sys.exit(1)

        self.lock = lock
        self.count = 0
        self.target = target

    def set_target(self, target):
        if target is None:
            return False
        else:
            self.target = target
            return True

    def recv(self):
        return self.sock.recvfrom(512)[0]

    def inspect(self, rsp, min_addr, max_addr):
        pass

    def output(self):
        pass

    def recvloop(self):
        global scan_stop
        status, ip_range = iprange(self.target[0])
        if ip_range is None:
            print "Syntax error!"
            return status
        elif status:
            while not scan_stop:
                try:
                    self.ip_addr = ip_range[0]
                    if self.inspect(self.recv(), ipmin(ip_range), ipmax(ip_range)):
                        self.output()
                except socket.error:
                    self.sock.close()
                    self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x03))
        else:
            while not scan_stop:
                try:
                    self.ip_addr = ip_range[0]
                    scan_stop =  self.inspect(self.recv(), None, None)
                    if scan_stop:
                        self.output()
                except socket.error:
                    scan_stop = True

        return self.postloop(scan_stop)

    def postloop(self, status):
        global scan_stop
        scan_stop = False
        return status

    def run(self):
        self.recvloop()

def scan(module_path, option):
    module = importmod(module_path)

    if module.scanner == "nostate":
        lock = threading.Lock()
        d = multiprocessing.Manager().dict()
        for key in option:
            d[key] = option[key]

        p = multiprocessing.Process(target=module.start, args=(lock, d))
        p.daemon = True

        p.start()
        p.join()

        return True
    else:
        return False
