#!/usr/bin/env python
#-*- coding:utf-8 -*-

import struct

from icscan.lib.net import IP, TCP
from icscan.lib.util.math import CRC

class Modbus(object):

    def __init__(self, TCP=None, tran_id=0, proto_id=0, slave_id=0, fn_code=0, data=""):
        
        self.TCP        = TCP
        self.data       = data
        self.tran_id    = tran_id
        self.proto_id   = proto_id
        self.header_len = len(self.data)+2
        self.slave_id   = slave_id
        self.fn_code    = fn_code

        if TCP is None:
            self.rebuild()
        else:
            self.repack()

    def repack(self, TCP=None, IP=None):
        
        if TCP is None:
            TCP = self.TCP
        else:
            self.TCP = TCP

        if IP is None:
            IP = TCP.IP
        else:
            TCP.IP = IP

        self.rebuild()
        self.TCP.data   = self.content
        self.TCP.repack()
        self.packet = self.TCP.segment

    def rebuild(self):
        self.header = struct.pack('!HHHBB', self.tran_id,
                                            self.proto_id,
                                            self.header_len,
                                            self.slave_id,
                                            self.fn_code
                                            )
        self.unheader = struct.pack('!HHHBB', self.header)

        self.content = self.header + self.data

