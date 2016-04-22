# -*- coding:utf-8 -*-

import os
import sys
import time
import socket
import struct

from icsuit.core import conf
from icsuit.core.nostate import Sender, Recver
from icsuit.core.cyclic import iprange, ipmask
from icsuit.lib.net import IP, TCP
from icsuit.lib.util.output import print_ip, print_tcp, column_print

scanner = "nostate"
option = {
    # scan options
    "BANDWIDTH": "10000",
    "TIMEOUT": "1",

    # output options
    "OUTPUT_FILE": "",

    # target options
    "TARGET_IP": "10.13.22.1/16",
    "TARGET_PORT": "6666",
    }


class TCPSYNSender(Sender):
    def __init__(self, lock, name, seed=None, rate=50, timeout=1, probe=None, target=None):
        Sender.__init__(self, lock, name, seed, rate, timeout, probe, target)

    def send(self, ip, port):
        return self.sock.sendto(build_probe(ip, port)[0], (ip, port))

    def postsend(self, status):
        mask = ipmask(iprange(self.target[0])[1])
        sys.stdout.write("\n\nbandwidth set %dp/s, %d hosts, cost: %d seconds.\n" % (self.rate, 2**mask, time.time()-self.begin))
        sys.stdout.flush()

        return status

    def run(self):
        self.sendloop()


class TCPSYNRecver(Recver):
    def __init__(self, lock, name, target=None, output_file=None):
        Recver.__init__(self, lock, name, target)
        self.output_file = output_file
        self.devices = []
    
    def inspect(self, rsp, min_addr, max_addr):
        # 解析以太网数据帧
        eth_len = 14
        eth_header = struct.unpack('!6s6sH', rsp[:eth_len])
        eth_protocol = socket.ntohs(eth_header[2])

        if eth_protocol != 8:
            return False

        # 解析IP首部
        ip_header = struct.unpack('!BBHHHBBH4s4s', rsp[eth_len:eth_len+20])
        ip_len = (ip_header[0] & 0x0f)*4
        ip_protocol = ip_header[6]
        ip_src = socket.inet_ntoa(ip_header[8])

        if ip_protocol != 6:
            return False
        elif min_addr is None:
            if ip_src != self.ip_addr:
                return False
        else:
            num = IP.ip2int(ip_src) 
            if num < min_addr or num > max_addr:
                return False

        # 解析TCP首部
        t = eth_len + ip_len
        tcp_header = struct.unpack('!HHLLBBHHH', rsp[t:t+20])
        src_port = tcp_header[0]
        if src_port != self.target[1]:
            return False
            
        if tcp_header[5] == 18:
            # 记录设备信息
            self.devices.append((ip_src, src_port, ip_header, tcp_header))
            return True

        return False

    def output(self):
        if self.output_file == None:
            return 
        else:
            path = os.path.join('/tmp', self.output_file)
            with open(path, 'a') as f:
                device = self.devices[-1]
                f.write("Host: %s\n" % device[0])
                f.write("="*65+"\n\n")
                probe, ip, tcp = build_probe(device[0], device[1])
                f.write("Send:\n")
                f.write("-----\n")
                print_ip(ip.unheader, out=f)
                print_tcp(tcp.unheader, out=f)
                f.write("Recv:\n")
                f.write("-----\n")
                print_ip(device[2], out=f)
                print_tcp(device[3], out=f)

    def postloop(self, status):
        global scan_stop
        scan_stop = False

        ip = []
        port = []
        status = []
        for device in self.devices:
            ip.append(device[0])
            port.append(str(device[1]))
            status.append("open")
        column_print(HOST_IP=ip, PORT=port, STATUS=status)

        with open('/tmp/data', 'w') as f:
            for device in self.devices:
                f.write("%s/%d\n" % (device[0], device[1]))
        
        return status

    def run(self):
        self.recvloop()


def build_probe(ip, port):
    src_ip = conf.LOCALHOST
    dst_ip = ip
    dst_port = port

    ip = IP.IP(src=src_ip, dst=dst_ip, protocol="tcp")
    tcp = TCP.TCP(IP=ip, dst_port=dst_port, flag_syn=1)

    return (tcp.segment, ip, tcp)
    
def parse_option(lock, option):
    # 选项解析
    args = {}
    args["target"] = (option["TARGET_IP"], int(option["TARGET_PORT"]))
    if option["OUTPUT_FILE"] != "None":
        args["output_file"] = option["OUTPUT_FILE"]

    recver = TCPSYNRecver(lock, "TCPSYNRecver", **args)

    args = {}
    args["target"] = (option["TARGET_IP"], int(option["TARGET_PORT"]))
    args["timeout"] = int(option["TIMEOUT"])

    probe_len = len(build_probe(option["TARGET_IP"].split('/')[0], int(option["TARGET_PORT"])))

    if option["BANDWIDTH"] != "":
        try:
            unit = option["BANDWIDTH"][-1]
            if unit == "P":
                rate = int(option["BANDWIDTH"][:-1])
                if rate > 11100:
                    args["rate"] = 40000
                else:
                    args["rate"] = rate
            elif unit == "K":
                rate = int(int(option["BANDWIDTH"][:-1])*1000/probe_len)
                if rate > 11100:
                    args["rate"] = 40000
                else:
                    args["rate"] = rate
            elif unit == "M":
                rate = int(int(option["BANDWIDTH"][:-1])*1000000/probe_len)
                if rate > 11100:
                    args["rate"] = 40000
                else:
                    args["rate"] = rate
            else:
                rate = int(option["BANDWIDTH"]) 
                if rate > 11100:
                    args["rate"] = 40000
                else:
                    args["rate"] = rate 
        except ValueError:
            print "Option 'BANDWIDTH' illegal, use the default setting."

    sender = TCPSYNSender(lock, "TCPSYNSender", **args)

    return (sender, recver)

def start(lock, option):
    sender, recver = parse_option(lock, option)
    if sender is None or recver is None:
        return False

    # 启动线程
    sender.start()
    recver.start()
    recver.join()
    sender.join()

    return True
