import subprocess
import os, signal
import time
import pygetch

# starting http
http = subprocess.Popen("python http.py", shell = True)
print 'started http with pid = ', http.pid
print "Kill all processes? (Y/N) "
#keystroke = pygetch()
#if keystroke is "Y" or keystroke is "y":
#	print "shutting down http"
#	http.kill()
