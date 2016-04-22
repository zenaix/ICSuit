# -*- coding: utf-8 -*-

import os
import sys
import pdb
import time
import socket
import unittest

from context import icsuit

from icsuit.lib.net import IP, TCP

def timeformat(second):
    s = ""
    if second / 3600 > 0:
        s += str(int(second / 3600))+"h "
        second = second % 3600
    if second / 60 > 0:
        s += str(int(second / 60))+"min "

    s += str(int(second % 60))+"s"
    
    return s

class TestLoader(unittest.TestCase):
    """Unit test cases for cli.loader."""

    def test_sock(self):
        os.chdir('..')
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        except socket.error, msg:
            print 'Create socket failed. Error code[%s], %s' % (str(msg[0]), msg[1])
            sys.exit(1)

        ip_src = '10.13.22.113'
        ip_dst = '10.13.22.196'
        dst_port = 6666
        ip = IP.IP(src=ip_src, dst=ip_dst, protocol='tcp')
        tcp = TCP.TCP(IP=ip, dst_port=dst_port, flag_syn=1)

        for i in range(10000, 111110):
            c = 6
            b = time.time()
            #e = 0
            e = time.time()
            count = 0
            while count < i*c:
                # 构造ip地址
                # ip_dst = IP.int2ip(((IP.ip2int(ip_dst) << 16) >> 16) + count%(2**16))
                if i < 10: 
                    time.sleep(round(0.99/i, 2)) 
                    sock.sendto(tcp.segment, (ip_dst, dst_port))
                elif i < 220:
                    if count % i == 0:
                        t = time.time()-e
                        if count != 0:
                            time.sleep(round((1-t), 2)) 
                        e = time.time()
                    sock.sendto(tcp.segment, (ip_dst, dst_port))
                elif i < 3300:
                    n = int(i/550)
                    if count % i == 0:
                        t = time.time()-e
                        time.sleep(round((1-n*0.01-t), 2)) 
                        e = time.time()
                    sock.sendto(tcp.segment, (ip_dst, dst_port))
                elif i < 16500:
                    n = int(i/1100)
                    if count % i == 0:
                        t = time.time()-e
                        time.sleep(round((1.0-n*0.01-t), 2)) 
                        e = time.time()
                    sock.sendto(tcp.segment, (ip_dst, dst_port))
                else:
                    if count % 9250 == 0:
                        time.sleep(0.01)
                    sock.sendto(tcp.segment, (ip_dst, dst_port))
                count += 1
                t = time.time() - b

                sys.stdout.write("%d%%[%s], Packets: %d, Rate: %dp/s, Rest time: %s\r" % (int(count*100/(i*c)), int(count*100/(i*c))*"#", count, round(float(count)/t), timeformat(int((c*i-count)*t/count))))
                #sys.stdout.flush()
            #sys.stdout.write("%d, %d\n" % (i, round(float(count/t))))
            sys.stdout.write("\n\n")
            sys.stdout.flush()

        os.chdir('tests')

if __name__ == '__main__':
    unittest.main()
