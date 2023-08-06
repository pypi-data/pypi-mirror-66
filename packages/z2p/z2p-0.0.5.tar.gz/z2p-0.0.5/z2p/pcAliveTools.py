'''
    检测pc是否存活的工具库

    pc是否存活的判断方式
'''
from scapy.all import *

def arpScan(ip,timeout=1):
    '''
    利用arp的方式，检查提供的ip地址是否存活
    Args：
        ip：
            type：str
            所要探测的ip地址
        
    Returns：
        True or False
        存活则返回True
    '''

    response=sr1(ARP(pdst=ip),timeout=timeout,verbose=0)
    if response:
        return True
    else:
        return False


def icmpScan(ip,timeout=1):

    '''
    利用icmp的方式，检查提供的ip地址是否存活
    Args：
        ip：
            type：str
            所要探测的ip地址
        
    Returns：
        True or False
        存活则返回True
    '''

    packet = IP(dst=ip)/ICMP()
    response = sr1(packet,timeout=timeout,verbose=False)
    if response:
        return True
    else:
        return False



if __name__ == '__main__':

    a = arpScan('192.168.3.9')
    # a = icmpScan('192.168.3.9')
    print(a)