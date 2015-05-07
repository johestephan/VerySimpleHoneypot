README - SendMeSpamIDS.py
====
IDS for analyzing mail and apache data

* mypyfwa - apache anayzer ./mypyfwa
* smsids - smtp daemon, accept all ./smsids
* virustotal - uploader and checker for virustotal ./virustotal


## Modules needed
* smtpd
* asyncore
* sqlite3 
* time
* pyclamd (needs clamav-daemon to be installed)
* geolite2 (needs GeoIP to be installed)
* logger
* sys
* optParser

all modules are normally installed using pip, like

'''
pip install --upgrade pyclamd
'''

## Toolbox
* added ./toolbox folder
* sendviagmail.py - little script to send emails via gmail
* logrotate.apache - entry from my logrotate, mailscript is used here

## How does it work
The script opens a connection and SMTP Server on port 1025 (for tests, should be changed to 25)
an accepts every mail which is send to the server. It than logs the data and some other
informations into an sqlite database.
It was created to help analyze SPAM and malware which is sended per mail.

## Status
* 03/18/2015 - switched from pyclamav to pyclamd, now scanning stream instead of file
* 03/20/2015 - pushed sqlite3 logging into own function, bug fixing
* 04/22/2015 - added syslog output, what is now default (-l option to enable sqllog)
* 05/07/2015 - added long verbose output for mailsending, added length analyzer for request
