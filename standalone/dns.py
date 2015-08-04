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
	rawf = open('/var/log/smsids_raw.log','a')
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        rawf.write('BEGIN OF DNS DATA:\n')
	rawf.write(st +'\n')
	rawf.write('Source IP: '+ addy[0] +'\n')
        rawf.write(xf +'\n')
	rawf.write(data + '\n END OF DATA\n')
	rawf.write('\n')
	rawf.close()
        # ters = mypyfwa.GETcheck(dataarray[0],addy[0])
        ters = (addy[0].strip(), str((len(data))))
        syslogit.logit("DNS", ters)
        con.send("Thanks for flying with us")
	con.close()
    except Exception, e:
	print e
	rawf.close()
	con.close()
