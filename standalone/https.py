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
import ssl


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveaddy = ('0.0.0.0', 2345)
sock.bind(serveaddy)
sock.listen(1)

while True:
    try:
        msg = ""
        con,addy = sock.accept()
	connstream = ssl.wrap_socket(con,
                                server_side=True,
                                certfile="certificate.crt",
                                keyfile="privateKey.key",
                                ssl_version=ssl.PROTOCOL_SSLv23)
        xf = "test" #IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
	data = connstream.read() # receive maximum 8K data
	print data
	dataarray = data.split('\n')
        rawf = open('/var/log/smsids_raw.log','a')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        rawf.write(st +'\n')
        rawf.write('Source IP: '+ addy[0] +'\n')
        rawf.write(xf +'\n')
        rawf.write(data + '\n END OF DATA\n')
        rawf.write('\n')
        rawf.close()
        ters = mypyfwa.GETcheck(dataarray[0],addy[0])
        syslogit.logit("http",' -- '.join(ters))
        connstream.write("HTTP/1.1 200 OK\n"
         +"Content-Type: text/html\n"
         +"\n" # Important!
         +"<html><body>Hello World</body></html>\n");
        con.close()
    except Exception, e:
        print e

