#!/bin/python

import simplejson
import urllib
import urllib2
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-u", "--url", dest="scanurl",
                  help="URL to be checked by Virustotal", metavar="scanurl")

(options, args) = parser.parse_args()


url = "https://www.virustotal.com/vtapi/v2/url/scan"
with open ("./apikey","r") as myapifile:
	apikey = myapifile.readline().strip()



parameters = { "url" : options.scanurl,
	       "apikey": apikey}

data = urllib.urlencode(parameters)
req = urllib2.Request(url,data)
response = urllib2.urlopen(req)
json = response.read()
print json
