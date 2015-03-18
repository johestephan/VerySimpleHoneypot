#!/usr/bin/python
#
# Copyright 2014 by Joerg Stephan <jost2208@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import smtpd
import asyncore
import sqlite3
import time
import pyclamav
from geoip import geolite2

class IDS_SMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
	Now=time.time()
	filename= "./tmp/"+ str(Now) + ".txt"

  	print 'ID		      ', Now
	print 'Timestamp	      ', time.strftime('%X %x %Z')
        print 'Receiving message from:', peer[0]
        match = geolite2.lookup(peer[0])
	if match is not None:
		Country = match.country
	else:
		Country = 'Unknown'

	print 'Country		: ', Country

	print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)
	print 'Message store location:', filename
	tempfile = open(filename, 'w')
	tempfile.write(data)
	tempfile.close()
	ret=pyclamav.scanfile(filename)
	print 'clamav		     :', ret

	conn = sqlite3.connect('smsids.db', isolation_level=None)
	c = conn.cursor()
	logrow= (Now,time.strftime('%X %x %Z'), peer[0], peer[1], Country, mailfrom,rcpttos[0],len(data),data,filename,ret[1])
	c.execute('''INSERT INTO log VALUES (?,?,?,?,?,?,?,?,?,?,?);''', logrow) 
	conn.commit
	conn.close
	return

print 'Server ready for connections...'
server = IDS_SMTPServer(('0.0.0.0', 1025), None)

asyncore.loop()
