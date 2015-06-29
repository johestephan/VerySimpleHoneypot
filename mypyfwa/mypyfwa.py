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

def GETcheck(request, IP, CC):
    try:
	weightcounter = request.count("/")
	if weightcounter > 7:
		print str(datetime.datetime.now()) + " " + request + " RecursiveCounter: " + str(weightcounter) + " Blocked: " + IP
                logit( (str(datetime.datetime.now()),request,IP,CC,"Path") )
		return True
	elif len(request) > 60:
		print str(datetime.datetime.now()) + " " + request + " LenCounter: " + str(weightcounter) + " Blocked: " + IP
                logit( (str(datetime.datetime.now()),request,IP,CC,"Length") )
                return True
	else:
		return False
    except:
	print "Unexpected error (GET_recursive):", sys.exc_info()[0]
        return False


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


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE, default is /var/log/mypyfw.log", metavar="FILE")
parser.add_option("-i", "--ippos", dest="IPpos", type="int",
		  help="adjust IP position, default is 0", metavar="IPPOSITION")
parser.add_option("-b", "--blacklist", dest="blacklist", default="./conf.d/MatchList",
		  help="path to blacklist, default values are Hardcoded", metavar="FILE")
parser.add_option("-w", "--whitelist", dest="whitelist", default="./conf.d/IPWhiteList",
		  help="path to Whitelist, default values are Hardcoded", metavar="FILE")
parser.add_option("-s", "--inputstream", dest="streamsource",
		  help="Apache Log file to follow stream", metavar="FILE")
parser.add_option("-l", "--logging",action="store_false", default=True, dest="syslog",
		  help="if set, old sqlite logging is used")


(options, args) = parser.parse_args()

blacklist = "Wget|Python|sqlmap|curl|apach0day|pma|php|connect|wordpress|wp"
whitelist = "127.0.0.1|::1"

# Parsing Options
if (options.filename is None): 
    options.filename = "./mypyfwa.log"

if (options.IPpos is None):
    options.IPpos = 1

if (options.blacklist is not None): 
    for line in open(options.blacklist, "r") :
        blacklist = blacklist +"|" + line.rstrip()
    print "extended Blacklist: " + blacklist
        
if (options.whitelist is not None): 
    for line in open(options.whitelist, "r") :
        whitelist = whitelist + "|" + line.rstrip()
    print "extended Whitelist: " + whitelist

logf = open(options.filename,'a')
sys.stdout = logf
recent = list()
counter = 0

injectcounter = 0
getcounter = 0
headercounter = 0

        
if (options.streamsource is not None):
	source = open(options.streamsource,'r')
else:
	source = sys.stdin

for line in source:
    # using a combined log line via regex
    #line = '172.16.0.3 - - [25/Sep/2002:14:04:19 +0200] "GET / HTTP/1.1" 401 - "" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1) Gecko/20020827"'
    regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
    dataset = re.match(regex, line)
    IP = dataset.groups()[0]
    match = geolite2.lookup(IP)
    if match is not None:
	CC = str(match.country)
    else:
        CC = "UNKNOWN"
   
    iires = re.search(whitelist,IP) 
    if ( iires is None ) :
	Request = dataset.groups()[2]
    	headercounter += HEADERanalyzer(line, IP, CC)
    	injectcounter += GETanalyzer(Request, line,  IP, CC)
    	getcounter += GETcheck(Request, IP, CC)  
    
    
logf.close()
sys.stdout = sys.__stdout__

print "Logged " + str(headercounter) + " Lines of bad headers"
print "Logged " + str(injectcounter) + " Lines of possible injections"
print "Logged " + str(getcounter) + " Lines of strange headers "
  
