from scapy.all import *


def updatePcapChecksum(packets):
    '''
    更新pcap包中的TCP checksum，并以list的方式返回，通过wrpcap就可重新生成pcap包

    Args：
        packets：
            type：scapy.plist.PacketList
            所要更新的pcap包内容

    Returns:
        []        
    '''
    lists = []
    for packet in packets:
        if packet.haslayer('TCP'):
            packet['TCP'].chksum = None

        lists.append(packet)
    
    return lists


def countPcapIPS(packets):
    '''
    检查pcap包中共有几个ip，并以list的方式返回

    Args：
        packets：
            type：scapy.plist.PacketList
            所要检查的pcap包内容
        
    Returns：
        []
        所有ip，去重返回，如['1.1.1.1','1.2.1.1','1.2.3.4']
    '''
    lists = []
    for packet in packets:
        if packet.haslayer('IP'):
            lists.append(packet['IP'].src)
            lists.append(packet['IP'].dst)
        elif packet.haslayer('IPv6'):
            lists.append(packet['IPv6'].src)
            lists.append(packet['IPv6'].dst)

    return list(set(lists))


def countPcapPorts(packet):
    '''
    检查pcap包中共有几个端口，并以list的方式返回

    Args：
        packets：
            type：scapy.plist.PacketList
            所要检查的pcap包内容
        
    Returns：
        []
        所有端口，去重返回，如[80,90,100,8080]
    '''
    lists = []
    for packet in packets:
        if packet.haslayer('TCP'):
            lists.append(packet['TCP'].sport)
            lists.append(packet['TCP'].dport)

    return list(set(lists))




if __name__ == '__main__':

    packets = rdpcap('/Users/z2p/Downloads/uridata_hex02_attack.pcap')
    # print(packets)
    # print(type(packets))
    a = countPcapPorts(packets)
    print(a)