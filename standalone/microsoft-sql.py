#!/usr/bin/python
#
# simple MS-SQL Server
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
serveaddy = ('0.0.0.0', 1433)
sock.bind(serveaddy)
sock.listen(1)

while True:
    try:
        msg = ""
        con,addy = sock.accept()
        xf = IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
        data = con.recv(24000) # receive maximum 24K data
        dataarray = data.split('\n')
	rawf = open('/var/log/smsids_raw.log','a')
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	rawf.write('BEGIN OF HTTP DATA:\n')
	rawf.write(st +'\n')
	rawf.write('Source IP: '+ addy[0] +'\n')
        rawf.write(xf +'\n')
	rawf.write(data + '\n END OF DATA\n')
	rawf.write('\n')
	rawf.close()
        # ters = mypyfwa.GETcheck(dataarray[0],addy[0])
	ters = (addy[0].strip() , str(len(data))) 
        syslogit.logit("MS-SQL", ters)
        con.send("Thanks for flying with us!")
	con.close()
    except Exception, e:
	print e
