import subprocess
import os, signal
import time
import sys
import psutil


def killchilds(cpid):
	p = psutil.Process(cpid)
        child_pid = p.children(recursive=True)
	os.kill(child_pid[0].pid,9)


# starting http
http = subprocess.Popen("python http.py", shell = True)
print 'started http with pid = ', http.pid
https = subprocess.Popen("python https.py", shell = True)
print 'started https with pid = ', https.pid
smtp = subprocess.Popen("python smtp.py -p 25", shell = True)
print 'started smtp with pid = ', smtp.pid
telnet = subprocess.Popen("python telnet.py", shell = True)
print 'started smtp with pid = ', telnet.pid



print "Kill all processes? (Y/N) "
keystroke = raw_input()
if keystroke is "Y" or keystroke is "y":
	print "shutting down http"
        killchilds(http.pid)
	http.terminate()
	print "shutting down https"
        killchilds(https.pid)
	https.terminate()
        print "shutting down smtp"
        killchilds(smtp.pid)
        smtp.terminate()
        print "shutting down telnet"
        killchilds(telnet.pid)
        telnet.terminate()


sys.exit
