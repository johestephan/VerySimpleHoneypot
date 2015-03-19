README - SendMeSpamIDS.py
====
Simple SMTP fetch all IDS and analyzer

## Modules needed
* smtpd
* asyncore
* sqlite3 
* time
* pyclamd (needs clamav-daemon to be installed)
* geolite2 (needs GeoIP to be installed)

all modules are normally installes using pip

## How does it work
The script opens a connection and SMTP Server on port 1025 (for tests, should be changed to 25)
an accepts every mail which is send to the server. It than logs the data and some other
informations into an sqlite database.
It was created to help analyze SPAM and malware which is sended per mail.

## Status
* 03/18/2015 - switched from pyclamav to pyclamd, no scanning stream instead of file