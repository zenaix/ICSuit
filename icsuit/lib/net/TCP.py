# -*- coding:utf-8 -*-

import socket
import struct
import random

from icsuit.lib.util.math import CRC

class TCP(object):
    
    def __init__ (self, IP, seq=0, ack=0, header_len=5, window_size=65535, **kw):
        
        self.IP             = IP
        self.src_port       = kw['src_port'] if 'src_port' in kw else random.randint(32767, 65535)
        self.dst_port       = kw['dst_port']
        self.seq            = random.randint(0, 4294967295) if seq == None else seq
        self.ack            = random.randint(0, 4294967295) if ack == None else ack
        self.header_len     = header_len

        self.flag_urg       = kw['flag_urg'] if 'flag_urg' in kw else 0
        self.flag_ack       = kw['flag_ack'] if 'flag_ack' in kw else 0
        self.flag_psh       = kw['flag_psh'] if 'flag_psh' in kw else 0
        self.flag_rst       = kw['flag_rst'] if 'flag_rst' in kw else 0
        self.flag_syn       = kw['flag_syn'] if 'flag_syn' in kw else 0
        self.flag_fin       = kw['flag_fin'] if 'flag_fin' in kw else 0

        self.window_size    = window_size 
        self.chksum         = 0
        self.urgent_ptr     = 0

        self.option         = kw['option'] if 'option' in kw else ""
        self.data           = kw['data'] if 'data' in kw else ""

        self.repack()

    def checksum (self, IP):
        """计算TCP首部校验和 
        """
        self.flags          = self.flag_fin + (self.flag_syn<<1) + (self.flag_rst<<2) + (self.flag_psh<<3) + (self.flag_ack<<4) + (self.flag_urg<<5)
        self.chksum         = 0

        tcp_header          = struct.pack('!HHLLBBHHH', self.src_port, 
                                                        self.dst_port, 
                                                        self.seq,
                                                        self.ack,
                                                        self.header_len<<4,
                                                        self.flags,
                                                        self.window_size,
                                                        self.chksum,
                                                        self.urgent_ptr
                                                        )

        # 构造IP伪首部
        pseudo_ip = struct.pack('!4s4sBBH', IP.src,
                                            IP.dst,
                                            0,
                                            IP.protocol,
                                            len(tcp_header) + len(self.option) + len(self.data)
                                            )
        
        msg = pseudo_ip + tcp_header + self.option + self.data
        if len(msg) % 2 != 0:
            msg += '\0'

        self.chksum = CRC(msg)

    def repack(self, IP=None):
        """封装TCP首部
        """
        if IP is None:
            IP = self.IP
        else:
            self.IP = IP

        self.checksum(IP)
            
        self.header = struct.pack('!HHLLBBHHH', self.src_port, 
                                                self.dst_port, 
                                                self.seq,
                                                self.ack,
                                                self.header_len<<4,
                                                self.flags,
                                                self.window_size,
                                                self.chksum,
                                                self.urgent_ptr
                                                )
        self.unheader = struct.unpack('!HHLLBBHHH', self.header)

        self.segment = IP.header + self.header + self.option + self.data
