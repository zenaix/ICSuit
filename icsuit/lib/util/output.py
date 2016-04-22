# -*- coding:utf-8 -*-

import sys
import socket
import struct


def timeformat(second):
    s = ""
    if second / 3600 > 0:
        s += str(int(second / 3600))+"h "
        second = second % 3600
    if second / 60 > 0:
        s += str(int(second / 60))+"min "

    s += str(int(second % 60))+"s"
                                               
    return s

def column_print(tab=True, ruler='-', **columns):
    # 检查参数合法性
    if columns is None:
        return False

    f = lambda x, y: y if len(x) == len(y) else [] 
    l = reduce(f, [columns[title] for title in columns])
    if l == []:
        return False
    else:
        l = len(l)

    m = {}
    for title in columns:
        m[title] = max(map(len, columns[title]+[title]))

    # 打印标题
    t = ""
    r = ""
    for title in columns:
        n = m[title] - len(title) + 2
        header = ' '.join(title.split('_'))
        t += header + n*' '
        r += ruler*len(title) + n*' '

    if tab:
        sys.stdout.write("\t%s\n" % t)
        sys.stdout.write("\t%s\n" % r)
    else:
        sys.stdout.write("%s\n" % t)
        sys.stdout.write("%s\n" % r)

    # 打印内容
    for i in range(l):
        s = ""
        for title in columns:
            n = m[title] - len(columns[title][i]) + 2
            s += columns[title][i] + n*" "

        if tab:
            sys.stdout.write("\t%s\n" % s)
        else:
            sys.stdout.write("%s\n" % s)

    sys.stdout.flush()

    return True
        
def print_eth(eth_header, out=sys.stdout):
    eth_protocol = socket.ntohs(eth_header[2])
    src_mac = eth_header[0].encode('hex')
    out.write("                                    Ethernet Header(14 bytes)                                    \n")
    out.write(" 0 1 2 3 4 5 6 7 8 9 a b c d e f 0 1 2 3 4 5 6 7 8 9 a b c d e f 0 1 2 3 4 5 6 7 8 9 a b c d e f \n")
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    out.write("|                                  src mac: %s:%s:%s:%s:%s:%s                                   |\n" % (src_mac[0:2], 
    src_mac[2:4], src_mac[4:6], src_mac[6:8], src_mac[8:10], src_mac[10:]))
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    dst_mac = eth_header[1].encode('hex')
    out.write("|                                  dst mac: %s:%s:%s:%s:%s:%s                                   |\n" % (dst_mac[0:2], 
    dst_mac[2:4], dst_mac[4:6], dst_mac[6:8], dst_mac[8:10], dst_mac[10:]))
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    out.write("|        protocol: ip(%s)        |\n"  % (str(eth_protocol)))
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    out.write("\n")

def print_ip(ip_header, out=sys.stdout):
    ip_len = (ip_header[0]&0x0f)*4
    out.write("                        IP Header(20 bytes)                      \n")
    out.write(" 0 1 2 3 4 5 6 7 8 9 a b c d e f 0 1 2 3 4 5 6 7 8 9 a b c d e f \n")
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    out.write("|version|   %s  |      tos      |      total length(%s)         |\n" % (ip_len, ip_header[2]))
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    l = len(str(ip_header[5]))
    s = str(ip_header[5]) + ")"+" "*(9-l)
    out.write("|      identification(%s|flags|     fragment offset     |\n" % s)
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    l = len(str(ip_header[5]))
    s = str(ip_header[5]) + ")"+" "*(7-l)
    out.write("|     TTL(%s| protocol(6) |         header checksum       |\n" % s)
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    ip_src = socket.inet_ntoa(ip_header[8])
    l = len(ip_src)
    s = ip_src+" "*(39-l)
    out.write("|                        %s|\n" % s)
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    ip_dst = socket.inet_ntoa(ip_header[9])
    l = len(ip_dst)
    s = ip_dst+" "*(39-l)
    out.write("|                        %s|\n" % s)
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    out.write("\n")

def print_tcp(tcp_header, out=sys.stdout):
    out.write("                       TCP Header(20 bytes)                      \n")
    out.write(" 0 1 2 3 4 5 6 7 8 9 a b c d e f 0 1 2 3 4 5 6 7 8 9 a b c d e f \n")
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    l = len(str(tcp_header[0]))
    src_port = str(tcp_header[0])+")"+" "*(15-l)
    l = len(str(tcp_header[1]))
    dst_port = str(tcp_header[1])+")"+" "*(15-l)
    out.write("|      src port(%s|      dst port(%s|\n" % (src_port, dst_port))      
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    l = len(str(tcp_header[2]))
    s = str(tcp_header[2])+")"+" "*(30-l)
    out.write("|                sequence number(%s|\n" % s)
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    l = len(str(tcp_header[3]))
    s = str(tcp_header[3])+")"+" "*(24-l)
    out.write("|                acknowledgment number(%s|\n" % s)
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")

    flag = {0:["U", "A", "P", "R", "S", "F"], 1:["R", "C", "S", "S", "Y", "I"], 2:["G", "K", "H", "T", "N", "N"]}
    flags = bin(tcp_header[5])[2:]
    l = len(flags)
    if l < 6:
        flags = "0"*(6-l)+flags
    for i in range(0, len(flags)):
        if flags[i] == "0":
            for key in flag:
                flag[key][i] = " "

    out.write("|  data |           |%s|%s|%s|%s|%s|%s|                               |\n" % tuple(flag[0]))
    out.write("|       | reserved  |%s|%s|%s|%s|%s|%s|         window size           |\n" % tuple(flag[1]))
    out.write("| offset|           |%s|%s|%s|%s|%s|%s|                               |\n" % tuple(flag[2]))
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    out.write("|           check sum           |        urgent pointer         |\n")
    out.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    out.write("\n")

if __name__ == '__main__':
    column_print(aaa_aaaa=['a', 'aa', 'aaa'], b=['b', 'bbbbbbbbbb', 'bbb'], c=['c', 'cc', 'ccc'])
