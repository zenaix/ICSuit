# -*- coding:utf-8 -*-

import random
import socket
import struct

from icsuit.lib.net.IP import ip2int, int2ip

table = {
    2:3,
    4:5,
    8:11,
    16:17,
    32:37,
    64:67,
    128:131,
    256:257,
    512:521,
    1024:1031,
    2048:2053,
    4096:4099,
    8192:8209,
    16384:16411,
    32768:32771,
    65536:65537,
    131072:131101,
    262144:262147,
    524288:524309,
    1048576:1048583,
    2097152:2097169,
    4194304:4194319,
    8388608:8388617,
    16777216:16777259,
    33554432:33554467,
    67108864:67108879,
    134217728:134217757,
    268435456:268435459,
    536870912:536870923,
    1073741824:1073741827,
    2147483648:2147483659,
    4294967296:4294967311,
}

def iprange(target):
    iprange = target.split('/')
    if len(iprange) == 1:
        return (False, iprange)
    elif len(iprange) == 2:
        return (True, iprange)
    else:
        return (False, None)
        
def ipmask(iprange):
    return 32 - int(iprange[1])

def ipmin(iprange):
    mask = ipmask(iprange)
    return (ip2int(iprange[0]) >> mask) << mask

def ipmax(iprange):
    mask = ipmask(iprange)
    min_addr = ipmin(iprange)
    return min_addr + 2**mask - 1

def ipcycle(iprange, seed=None):
    mask = 32 - int(iprange[1])
    min_addr = (ip2int(iprange[0]) >> mask) << mask

    prime = table[2**mask]
    seed = random.randint(1, 2**mask) if seed is None else seed

    for i in xrange(0, prime):
        mod = seed*i % prime
        if mod < 2**mask:
            yield int2ip(min_addr+mod)
        else:
            continue
