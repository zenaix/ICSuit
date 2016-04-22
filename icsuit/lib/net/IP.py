# -*- coding:utf-8 -*-

import socket
import struct

def ip2int(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(ip))[0])
    
def int2ip(num):
    return socket.inet_ntoa(struct.pack('I',socket.htonl(num)))

class IP(object):
    
    def __init__(self, version=4, header_len=5, tos=0, ipid=0, flags=0, offset=0, ttl=255, checksum=0, **kw):

        self.version     = version
        self.header_len  = header_len
        self.tos         = tos
        self.total_len   = 44
        self.ipid        = ipid
        self.flags       = flags
        self.offset      = offset
        self.ttl         = ttl
        self.protocol    = socket.IPPROTO_TCP if kw['protocol'] == 'tcp' else socket.IPPROTO_UDP
        self.checksum    = checksum
        self.src         = socket.inet_pton(socket.AF_INET, kw['src'])
        self.dst         = socket.inet_pton(socket.AF_INET, kw['dst'])

        self.repack()

    def repack(self):
        """封装IP首部
        """
        self.header = struct.pack('!BBHHHBBH4s4s', (self.version << 4) + self.header_len,
                                                    self.tos,
                                                    self.total_len,
                                                    self.ipid,
                                                    (self.flags << 5) + self.offset,
                                                    self.ttl,
                                                    self.protocol,
                                                    self.checksum,
                                                    self.src,
                                                    self.dst
                                                   )
        self.unheader = struct.unpack('!BBHHHBBH4s4s', self.header)
