# -*- coding:utf-8 -*-

import fcntl
import socket
import struct

def get_ip_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])

LOCALHOST = get_ip_addr('eth0')
module = {
    "probe/nostate/tcpsyn":"TCP SYN scan probe module, supported global size scan.",
    "probe/connect/modbus":"Modbus device information gathering module, based on TCP connection",
}

if __name__ == "__main__":
    print get_ip_addr('eth0')
