#!/usr/bin/python
# 
# V1-0 by Joerg Stephan <joerg DOT stephan AT ymail DOT com>
# https://github.com/johestephan/mypyapachefw.git
# Copyright (c) 2014,2015 Joerg Stephan under BSD licence
#

import sys
import re
import datetime
from optparse import OptionParser
from geoip import geolite2
import sqlite3
sys.path.append('../modules/')
import syslogit

def logit(data):
	try:
		
		if (options.syslog):
			print syslogit.logit("[mypyfwa]", data)
		else:
			# logging to sqlite3
			conn = sqlite3.connect('./mypyfwa.db')
			conn.execute(''' INSERT INTO log VALUES (?,?,?,?,?); ''', data) 
			conn.commit()
			conn.close()
		return 1
	except:
		return 0

def GETcheck(request, IP, CC=None):
    try:
	weightcounter = request.count("/")
	if weightcounter > 7:
		print str(datetime.datetime.now()) + " " + request + " RecursiveCounter: " + str(weightcounter) + " Blocked: " + IP
                ret = [str(datetime.datetime.now()),IP,request,"Path"] 
		return ret
	elif len(request) > 60:
		print str(datetime.datetime.now()) + " " + request + " LenCounter: " + str(weightcounter) + " Blocked: " + IP
                ret = [str(datetime.datetime.now()),IP, request,"Length"] 
                return ret
	else:
		return [str(datetime.datetime.now()), IP, request, "None"]
    except:
	print "Unexpected error (GET_recursive):", sys.exc_info()[0]
        return ["Error","None"]


def GETanalyzer(request, line, IP, CC):
    try:
	weightcounter = 0
	weightcounter2 = 0
	infectionlist1 = ["select","union","from","where","join"]
	infectionlist2 = ["echo","wget","curl","bash"]
	for rule in infectionlist1:
	    imatch = re.search(rule,request)
	    if imatch is not None:
	        weightcounter +=1
        for rule in infectionlist2:
            imatch = re.search(rule,line)
            if imatch is not None:
                weightcounter2 +=1

	if weightcounter > 1:
	    if re.match(r"select (?:[^;]|(?:'.*?'))* from", request) is not None:
	        print str(datetime.datetime.now()) + " " + request + " InjectCounter: " + str(weightcounter) + " Blocked: " + IP
            	logit( (str(datetime.datetime.now()),request,IP,CC,"SQLinjection") )
 	if weightcounter2 > 1:
            print str(datetime.datetime.now()) + " " + line + " InjectCounter: " + str(weightcounter) + " Blocked: " + IP
            logit( (str(datetime.datetime.now()),line,IP,CC,"SHELLinjection") )

	if ( weightcounter > 1) or (weightcounter2 > 1):		
	    return True
	else:
            return False
    except:
        print "Unexpected error (GET):", sys.exc_info()[0]
        return False


def HEADERanalyzer(line, IP, CC):
    try:
	xcounter = 0
	Request = line.split('"')[1].lower()
	Client = line.split('"')[-2]
	logstring = str(datetime.datetime.now()) + " " + IP + " Header: " + Client 
	m = re.search(blacklist,Client) # related services
	i = re.search(whitelist,IP) # Whitelabeld IP's
	if ( m is not None):
		logstring += " Matched Rule: " + str(m.group(0)) 
		print logstring
		xcounter += 1
       		logit( (str(datetime.datetime.now()),Client,IP,CC,"Scanner") )
		
	return xcounter
    except:
        print "Unexpected error (Header):", sys.exc_info()
        return 0


blacklist = "Wget|Python|sqlmap|curl|apach0day|pma|php|connect|wordpress|wp"
whitelist = "127.0.0.1|::1"

