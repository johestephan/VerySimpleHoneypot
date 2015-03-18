README - SendMeSpamIDS.py
====
Simple SMTP fetch all IDS and analyzer

## Modules needed
'''
import smtpd
import asyncore
import sqlite3
import time
import pyclamav
from geoip import geolite2
'''

## How does it work
The script opens a connection and SMTP Server on port 1025 (for tests, should be changed to 25)
an accepts every mail which is send to the server. It than logs the data and some other
informations into an sqlite database.
It was created to help analyze SPAM and malware which is sended per mail.