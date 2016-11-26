#!/usr/bin/python
#
# simple TELNET Server
# as Part of SendMeSpamIDS

import socket
import sys
sys.path.append('../modules/')
import syslogit
import mypyfwa
import datetime
import time



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveaddy = ('0.0.0.0', 2323)
sock.bind(serveaddy)
sock.listen(1)

while True:
    try:
        msg = ""
        con,addy = sock.accept()
        con.send("\n\nUser Access verification\n\n")
        con.send("login:")
        login = con.recv(20) # receive maximum 8K data
        con.send("password:")
        password = con.recv(20) # receive maximum 8K data
        con.send("\n\nCISCO-857# ")
        data = con.recv(8192)
        logit.log("TELNET", addy[0], data)
        con.send("Thanks for flying with us!\n")
        con.close()
    except Exception, e:
        print e
