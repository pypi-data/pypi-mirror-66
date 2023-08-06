'''
    检测端口开放情况的工具库
'''
from scapy.all import *
import random

def tcpConnectScan(ip,ports=[135,139],timeout=5):

    '''
    半开扫描，只发送syn，不会进行完整三次握手
    Args：
        ip：
            type：str
            所要探测的ip地址
        
    Returns：
        True or False
        存活则返回True
    '''
    for port in ports:
        packets = IP(dst=ip)/TCP(dport=port,flags='SU',urgptr=1,reserved=1,seq=random.randint(300000000,3253687545))
        res = sr1(packets,timeout=timeout,verbose=False)
        if res:
            return True
    
    return False


# def udpScan(ip,ports=[53,3389,9090,135,139],timeout=5):

#     for port in ports:
#         packets = IP(dst=ip)/UDP(dport=port)
#         res = sr1(packets,timeout=timeout,verbose=False)
#         if res == None:
#             print(port)
    

if __name__ == '__main__':

    a = tcpConnectScan('192.168.3.9')
    # a = udpScan('192.168.3.9')
    print(a)
