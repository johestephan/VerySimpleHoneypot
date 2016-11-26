#!/usr/bin/python
#
# simple DNS Server
# as Part of SendMeSpamIDS

import socket
import sys
sys.path.append('../modules/')
import syslogit
import IXFcheckMod
import mypyfwa
import datetime
import time



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serveaddy = ('0.0.0.0', 53)
sock.bind(serveaddy)

while True:
    try:
        msg = ""
        data,addy = sock.recvfrom(1024)
        xf = IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
        dataarray = data.split('\n')
        logit.log("DNS", addy[0], data)
        con.send("Thanks for flying with us")
	con.close()
    except Exception, e:
	print e
	rawf.close()
	con.close()
