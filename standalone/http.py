#!/usr/bin/python
#
# simple HTTP Server
# as Part of SendMeSpamIDS

import socket
import sys
sys.path.append('../modules/')
import syslogit
import IXFcheckMod

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveaddy = ('0.0.0.0', 2345)
sock.bind(serveaddy)
sock.listen(1)

while True:
    msg = ""
    con,addy = sock.accept()
    msg += addy[0] + " -- " + IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
    data = con.recv(8192) # receive maximum 8K data
    print addy
    print data
    con.sendall('HTTP/1.1 301 Moved Permanently')
    
