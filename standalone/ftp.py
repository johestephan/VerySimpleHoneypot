#!/usr/bin/python
#
# simple FTP Server
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
serveaddy = ('0.0.0.0', 20)
sock.bind(serveaddy)
sock.listen(1)

while True:
    try:
        msg = ""
        con,addy = sock.accept()
        data = con.recv(32000) # receive maximum 8K data
        logit.log("FTP", addy[0], data)
        con.send("Tanks for flying with us")
	con.close()
    except Exception, e:
	print e
	con.close()
	rawf.close()
