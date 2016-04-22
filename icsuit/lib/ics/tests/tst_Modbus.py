#!/usr/bin/env python
#-*- coding:utf-8 -*-

import socket
import struct
import unittest

from icscan.lib.net import IP, TCP
from icscan.lib.ics import Modbus

class tstModbus(unittest.TestCase):
    
    def setUp(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.r = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            self.e = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x03))
        except socket.error, msg:
            print 'Create socket failed. Error code[%s], %s' % (str(msg[0]), msg[1])
            sys.exit(1)

        self.src = '10.13.22.113'
        self.dst = '10.79.223.247'
        self.port = 502
        self.ip = IP.IP(src=self.src, dst=self.dst, protocol='tcp')
        self.tcp = TCP.TCP(IP=self.ip, dst_port=self.port, flag_syn=1)

    def test_init(self):
        modbus = Modbus.Modbus(TCP=self.tcp)

        self.assertEquals(modbus.TCP, self.tcp)
        self.assertEquals(modbus.content, self.tcp.data)
        self.assertEquals(modbus.packet, self.tcp.segment)

    def test_build(self):
        modbus = Modbus.Modbus(TCP=None)
        
        self.s.connect((self.dst, self.port))
        self.s.send(modbus.content)
        rsp = self.s.recv(1024)

        self.assertNotEquals(rsp, None)

    def test_pack(self):
        modbus = Modbus.Modbus(TCP=self.tcp)
        self.r.sendto(modbus.packet, (self.dst, 502))

        while True:
            rsp = self.e.recvfrom(65535)[0]

            eth_len         = 14
            eth_header      = struct.unpack('!6s6sH', rsp[:eth_len])
            eth_protocol    = socket.ntohs(eth_header[2])
            
            if eth_protocol != 8:
                continue
            
            ip_header       = struct.unpack('!BBHHHBBH4s4s', rsp[eth_len:eth_len+20])
            ip_len          = (ip_header[0]&0xf)*4
            ip_protocol     = ip_header[6]
            ip_src          = socket.inet_ntoa(ip_header[8])
            
            if ip_src != self.dst:
                continue
            elif ip_protocol != 6:
                continue

            t               = eth_len+ip_len  
            tcp_header      = struct.unpack('!HHLLBBHHH', rsp[t:t+20])
            tcp_flags       = tcp_header[5]
            tcp_port        = tcp_header[0]

            if tcp_port != 502:
                continue
            else:
                break

        self.assertEquals(tcp_flags, 18)

    def tearDown(self):
        self.s.close()
        self.r.close()
        self.e.close()
            
