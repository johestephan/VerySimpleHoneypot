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
serveaddy = ('0.0.0.0', 443)
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
        xf = IXFcheckMod.get_ip_intel_artillery_strip(addy[0])
	data = connstream.read() 
	dataarray = data.split('\n')
        rawf = open('/var/log/smsids_raw.log','a')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        rawf.write('BEGIN OF HTTPS DATA:\n')
        rawf.write(st +'\n')
        rawf.write('Source IP: '+ addy[0] +'\n')
        rawf.write(xf +'\n')
        rawf.write(data + '\n END OF DATA\n')
        rawf.write('\n')
        rawf.close()
        ters = (addy[0].strip(), str(len(data)))
        syslogit.logit("HTTPS", ters)
        connstream.write("HTTP/1.1 401 Unauthorized\n"
        + "Server: Apache/2.2.31 (Gentoo)"
        + "Accept-Ranges: bytes"
        + "Vary: Accept-Encoding"
        + "Content-Type: text/html"
         +"\n" # Important!
         +"<html><body>Wallistero.biz internal server</body></html>\n");
        con.close()
    except Exception, e:
        print e

