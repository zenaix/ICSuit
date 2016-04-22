# -*- coding:utf-8 -*-

def CRC(msg):
    """计算CRC校验和
    """
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i+1]) + (ord(msg[i]) << 8)
        t = s + w
        s = (t & 0xffff) + (t >> 16)

    return (~s & 0xffff)
