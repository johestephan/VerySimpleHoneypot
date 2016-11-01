import subprocess
import os, signal
import time
import sys
import psutil

services = {"http": ["http.py"],
		"https": ["https.py"],
		"smtp": ["smtp.py", "-p 25"],
		"Tomcat": ["tomcat.py"],
		"Telnet": ["telnet.py"],
		#"FTP": ["ftp.py"],
		#"DNS": ["dns.py"],
		#"MongoDB": ["mongodb"],
		#"RDP": ["rdp.py"],
		#"Oracle DB": ["oracle.py"],
		#"Microsoft SQL" :["microsoft-sql.py"],
		#"Microsoft DS": ["microsoft-ds.py"],
		}

pidSafe = {}

process = {}

#def killchilds(cpid):
#	p = psutil.Process(cpid)
#    child_pid = p.children(recursive=True)
#	os.kill(child_pid[0].pid,9)

def stop():
	for service in process:
		process[service].terminate()

def start():
	for service in services:
		if len(services[service]) > 1:
			options = " ".join(services[service][0:])
		else:
			options = services[service][0]
		try:
			if service in process:
				if process[service].poll() == 0:
					thisprocess = subprocess.Popen("python %s" % options, shell = True)
					process.update({service: thisprocess})
					print "Starting %s with PID %s" % (service, thisprocess.pid)
			else:
				thisprocess = subprocess.Popen("python %s" % options, shell = True)
				process.update({service: thisprocess})
				print "Starting %s with PID %s" % (service, thisprocess.pid)
		except:
			print "Error starting %s" % service
			continue
	print "DEBUG:" + str(process)
		


while (True):
	start()
	print "Kill all processes? (Y/N) "
	keystroke = raw_input()
	if keystroke is "Y" or keystroke is "y":
		stop()
		sys.exit()
