#!/usr/bin/python
#
# simple HTTP Server
# as Part of SendMeSpamIDS

import socket
import sys
import ssl

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveaddy = ('0.0.0.0', 2345)
sock.bind(serveaddy)
sock.listen(1)
ssl.wrap_socket(sock, ssl_version="TLSv1", ciphers="ADH-AES256-SHA")

while True:
    con,addy = sock.accept()
    data = con.recv(8192) # receive maximum 8K data
    sock.shutdown(1)
    print data
    
