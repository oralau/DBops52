#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import fcntl
import struct


# 多网卡情况下，根据前缀获取IP（Windows 下适用）

class GetIp:

    def get_ip_address_by_prefix(self,prefix):
        localIP = ''
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip.startswith(prefix):
                localIP = ip
        return localIP





    def get_ip_address_by_dev(self,dev_name):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', dev_name[:15])
        )[20:24])

