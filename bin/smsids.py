import time
import sys
import psutil
import threading
sys.path.append("../lib/")
import server as SC
import responses as RE

services = [["http", 8000, RE.DLink_200],
		["7547", 7547, RE.generic],
		["telnet", 23, RE.generic],
		["DLink_1", 52869, RE.generic]]

pidSafe = {}

process = {}


def stop():
	for service in process:
		print "Stopping process %s" % service
		process[service].do_run = False
		process[service].join()
		print process[service].isAlive()

def start():
	du_run = True
	for service in services:
		print "Starting Service  %s ..." % service[0]
		this = threading.Thread(target=SC.run, args=(service[0],service[1],service[2]))
		this.start()
		process.update({service[0]: this})
		


while (True):
	start()
	print str(process)
	print "Kill all processes? (Y/N) "
	keystroke = raw_input()
	if keystroke is "Y" or keystroke is "y":
		stop()
		sys.exit()
