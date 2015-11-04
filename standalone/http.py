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
        xf = IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
        data = con.recv(16000) # receive maximum 16K data
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
        syslogit.logit("HTTP", ters)
        con.send("HTTP/1.1 200 OK\n"
         +'''Date: Wed, 04 Nov 2015 16:42:19 GMT
Server: Apache/2.4.7 (Ubuntu)
Last-Modified: Wed, 04 Nov 2015 16:10:16 GMT
ETag: "cedc-523b93efdde53"
Accept-Ranges: bytes
Content-Length: 198
Vary: Accept-Encoding
Cache-Control: max-age=3600
Expires: Wed, 04 Nov 2015 17:42:19 GMT
Content-Type: text/html'''
         +"\n" # Important!
         +"<html><body>Wallistero.biz internal server - HTTPS only</body></html>\n");
	con.close()
    except Exception, e:
	    print e
