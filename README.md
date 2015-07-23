README - SendMeSpamIDS.py
====
IDS for analyzing mail and apache data

* run ./standalone/CommandControl.py as sudo to start all services


## Modules needed
* smtpd
* asyncore
* sqlite3 
* time
* pyclamd (needs clamav-daemon to be installed)
* geolite2 (needs GeoIP to be installed)
* logger
* sys

all modules are normally installed using pip, like

pip install --upgrade pyclamd

## Toolbox
* added ./toolbox folder
* sendviagmail.py - little script to send emails via gmail
* logrotate.apache - entry from my logrotate, mailscript is used here
* logstash configuration files

## How does it work
The software launches several silly TCP servers which pretend to be different types of services
Currently including
* HTTP
* HTTPS
* TELNET
* MONGODB (alpha state)
* RDP (alpha state)
* Microsoft DS (alpha state)
* Microsoft SQL (alpha state)
