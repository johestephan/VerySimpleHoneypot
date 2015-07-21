#!/usr/bin/python

import netaddr

def IP_Net(ip):
     if netaddr.IPAddress(ip) in netaddr.IPNetwork('10.0.0.0','8'):
         return True
     elif netaddr.IPAddress(ip) in netaddr.IPNetwork('172.16.0.0','12'):
	 return True
     elif netaddr.IPAddress(ip) in netaddr.IPNetwork('192.168.0.0','16'):
	 return True
     elif netaddr.IPAddress(ip) in netaddr.IPNetwork('127.0.0.1','8'):
	 return True
     else:
	 return False

