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
#smtp = subprocess.Popen("python smtp.py -p 25", shell = True)
#print 'started smtp with pid = ', smtp.pid
#telnet = subprocess.Popen("python telnet.py", shell = True)
#print 'started telnet with pid = ', telnet.pid
#mongodb = subprocess.Popen("python mongodb.py", shell = True)
#print 'started mongodb with pid = ', mongodb.pid
#oracle = subprocess.Popen("python oracle.py", shell = True)
#print 'started Oracle with pid = ', oracle.pid
#rdp = subprocess.Popen("python rdp.py", shell = True)
#print 'started rdp with pid = ', rdp.pid
#mssql = subprocess.Popen("python microsoft-sql.py", shell = True)
#print 'started Microsoft-SQL with pid = ', mssql.pid
#ftp = subprocess.Popen("python ftp.py", shell = True)
#print 'started FTP with pid = ', ftp.pid
#dns = subprocess.Popen("python dns.py", shell = True)
#print 'started DNS with pid = ', dns.pid
#tomcat = subprocess.Popen("python tomcat.py", shell = True)
#print 'started tomcat(8080) with pid = ', tomcat.pid



print "Kill all processes? (Y/N) "
keystroke = raw_input()
if keystroke is "Y" or keystroke is "y":
	print "shutting down http"
        killchilds(http.pid)
	http.terminate()
	print "shutting down https"
        killchilds(https.pid)
	https.terminate()
        #print "shutting down smtp"
        #killchilds(smtp.pid)
        #smtp.terminate()
        #print "shutting down telnet"
        #killchilds(telnet.pid)
        #telnet.terminate()
        #print "shutting down mongodb"
        #killchilds(mongodb.pid)
        #mongodb.terminate()
        #print "shutting down tomcat"
        #killchilds(tomcat.pid)
        #tomcat.terminate()
	#print "shutting down oracle"
        #killchilds(oracle.pid)
        #oracle.terminate()
        #print "shutting down ms-ds"
        #killchilds(msds.pid)
        #msds.terminate()
        #print "shutting down ms-sql"
        #killchilds(mssql.pid)
        #mssql.terminate()
        #print "shutting down ftp"
        #killchilds(ftp.pid)
        #ftp.terminate()
#        print "shutting down dns"
#        killchilds(dns.pid)
#        dns.terminate()
#        print "shutting down fake 8080"
#        killchilds(fakeeigthy.pid)
#        fakeeigthy.terminate()






sys.exit
