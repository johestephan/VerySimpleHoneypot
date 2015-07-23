#!/usr/bin/python
#
# simple TELNET Server
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
serveaddy = ('0.0.0.0', 23)
sock.bind(serveaddy)
sock.listen(1)

while True:
    try:
        msg = ""
        con,addy = sock.accept()
        xf = IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
	con.send("\n\nUser Access verification\n\n")
	con.send("login:")
        login = con.recv(20) # receive maximum 8K data
	con.send("password:")
        password = con.recv(20) # receive maximum 8K data
	con.send("\n\nCISCO-857# ")
	data = con.recv(8192)
	data += "User: " + login.strip() +"\nPass: " + password.strip() + "\n"
        dataarray = data.split('\n')
	rawf = open('/var/log/smsids_raw.log','a')
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        rawf.write('BEGIN OF TELNET DATA:\n')
	rawf.write(st +'\n')
	rawf.write('Source IP: '+ addy[0] +'\n')
        rawf.write(xf +'\n')
	rawf.write(data + '\n END OF DATA\n')
	rawf.write('\n')
	rawf.close()
        ters = (addy[0].strip(), str(len(data)))
        syslogit.logit("TELNET", ters)
        con.send("Thanks for flying with us!\n")
	con.close()
    except Exception, e:
	print e
