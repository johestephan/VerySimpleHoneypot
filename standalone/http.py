#!/usr/bin/python
#
# simple HTTP Server
# as Part of SendMeSpamIDS

import socket
import sys
sys.path.append('../modules/')
import logit
import mypyfwa
import datetime
import time



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveaddy = ('0.0.0.0', 80)
sock.bind(serveaddy)
sock.listen(1)

while True:
    try:
        msg = ""
        con,addy = sock.accept()
        #xf = IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
        data = con.recv(16000) # receive maximum 16K data
        dataarray = data.split('\n')
        logit.log("HTTP", addy[0], data)
        con.send("HTTP/1.1 200 OK\n"
        + "Server: Apache/2.2.31 (Gentoo)\n"
        + "Accept-Ranges: bytes\n"
        + "Vary: Accept-Encoding\n"
        + "Content-Type: text/html\n"
        +"\n" # Important!
        +"<html><body>Wallistero.biz internal server</body></html>\n")
    	con.close()
    except Exception, e:
	print e
	continue
