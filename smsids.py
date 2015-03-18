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

class IDS_SMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
	Now=time.time()
	filename= "./tmp/"+ str(Now) + ".txt"
  	print 'ID		      ', Now
	print 'Timestamp	      ', time.strftime('%X %x %Z')
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)
	print 'Message		     :', data
	print 'Message store location:', filename
	tempfile = open(filename, 'w')
	tempfile.write(data)
	tempfile.close()
	ret=pyclamav.scanfile(filename)
	print 'clamav		     :', ret
        return

print 'Server ready for connections...'
server = IDS_SMTPServer(('0.0.0.0', 1025), None)

asyncore.loop()
