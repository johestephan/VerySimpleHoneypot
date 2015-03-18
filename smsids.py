#!/usr/bin/python
#
# Copyright 2014 by Joerg Stephan <jost2208@gmail.com>
#

import smtpd
import asyncore
import sqlite3
import time
import pyclamav

class IDS_SMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)
	print 'Message		     :', data
	ret=pyclamav.scanthis(data)
	print 'clamav		     :', ret
        return

print 'Starting Server...'
server = IDS_SMTPServer(('0.0.0.0', 1025), None)

asyncore.loop()
