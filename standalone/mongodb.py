#!/usr/bin/python
#
# simple MONGODB Server
# as Part of SendMeSpamIDS

import socket
import sys
sys.path.append('../modules/')
import syslogit
import IXFcheckMod
import mypyfwa
import datetime
import time



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveaddy = ('0.0.0.0', 27017)
sock.bind(serveaddy)
sock.listen(1)

while True:
    try:
        msg = ""
        con,addy = sock.accept()
        xf = IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
        data = con.recv(8192) # receive maximum 8K data
        dataarray = data.split('\n')
    	logit.log("MONGODB", addy[0], data)
        con.send("Thanks for flying with us")
	con.close()
    except Exception, e:
	print e
