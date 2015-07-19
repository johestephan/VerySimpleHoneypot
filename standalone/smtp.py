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

from optparse import OptionParser
import sys
import smtpd
import asyncore
import sqlite3
import time
import pyclamd
from geoip import geolite2
import re
sys.path.append('../modules/')
import syslogit

def logit(data):
	# function to log to sqlite db
	#
	try:

		if (options.syslog):
			syslogit.logit("smtp", data)
		else:
			# logging to sqlite3
			conn = sqlite3.connect('./smsids.db')
			conn.execute(''' INSERT INTO log VALUES (?,?,?,?,?,?,?,?,?,?,?); ''', data) 
			conn.commit()
			conn.close()

		return 1
	except:
		return 0
		
def clamalyze(data):
	# function to handle check for malware
	# uses clamd and data as input stream
	try:
		clamd = pyclamd.ClamdAgnostic()
		ret = clamd.scan_stream(data)['stream']
		return ret
	except pyclamd.ConnectionError:
		print 'error connecting to clamd'
	except:
		return ('nope','nope')
	

class IDS_SMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
	# we need a whitelist, I finaly found out
	whitelist = "osml|js"
	i = re.search(whitelist,rcpttos[0]) # Whitelabeld IP's
	if ( i is None):
		# Creating timestamp now, this represents ID and filename
		Now=time.time()
		filename= "./tmp/"+ str(Now) + ".msg"
		outfile = open(filename,"w")
		outfile.write(data)
		# standard console output
		# includes some basic features which are also written to sqlite
  		print 'ID		      ', Now
		print 'Timestamp	      ', time.strftime('%X %x %Z')
        	print 'Receiving message from:', peer[0]
        	match = geolite2.lookup(peer[0])
		# GeoIP return must be check against None. Cause local IP addresses would cause an NoneObject Type and crash
		# the script.
		if match is not None:
			Country = match.country
		else:
			Country = 'Unknown'

		print 'Country		: ', Country

		print 'Message addressed from:', mailfrom
        	print 'Message addressed to  :', rcpttos[0]
        	print 'Message length        :', len(data)
		# clamav scan
		ret = clamalyze(data) 
		print 'clamav		     :', ret
	
		# Open sqlite db file and send data to it
		# Values are like
		# ID - represented via Unix-Timestamp
		# time - via current time
		# IP - the remote IP of the sender, peer[0]
		# port - port used by sender , peer[1]
		# Country Code - via GeoIP match.country
		# mailfrom - the sender email addy
		# rcpttos - to whom the mail was send
		# len(data) - the length (chars) of the origin data msg
		# data	- the data itself
		# filename - file the data was saved to (needed for clamav scan), format always /tmp/ID.txt
		# ClamAv return - what ClamAV has found
		#logrow = ( str(Now),time.strftime('%X %x %Z'), peer[0], peer[1], Country, mailfrom,rcpttos[0],str(len(data)),data,filename,ret[1]) 
		logrow = ( peer[0], Country, str(mailfrom),str(rcpttos[0]),str(len(data)),ret[1], filename) 
		print 'Logged?		:', logit(logrow)
		return

parser = OptionParser()
parser.add_option("-p", "--port", dest="port",
		  help="which port should be used , default 25", type=int, metavar="PORT", default=25)
parser.add_option("-l", "--logging",action="store_false", default=True, dest="syslog",
		  help="if set, old sqlite logging is used")


(options, args) = parser.parse_args()


print 'Server ready for connections...'
server = IDS_SMTPServer(('0.0.0.0', options.port), None)

asyncore.loop()
