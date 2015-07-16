#!/usr/bin/python
#
# simple HTTP Server
# as Part of SendMeSpamIDS

import socket
import sys
sys.path.append('../modules/')
import syslogit
import IXFcheckMod
import mypyfwa



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveaddy = ('0.0.0.0', 80)
sock.bind(serveaddy)
sock.listen(1)

while True:
    try:
        msg = ""
        con,addy = sock.accept()
        xf = IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
        data = con.recv(8192) # receive maximum 8K data
        dataarray = data.split('\n')
	rawf = open('/var/log/smsids_raw.log','a')
        rawf.writeline(xf)
	rawf.write(data)
	rawf.close()
        ters = mypyfwa.GETcheck(dataarray[0],addy[0])
        syslogit.logit("http",' -- '.join(ters))
        con.send(r'''HTTP/1.0 200 OK 
		   Content-Type: text/plain''')
    except:
        continue 
