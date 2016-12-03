README - SendMeSpamIDS.py
====
Honeypot for analyzing  data

* run ./bin/smsids.py as sudo to start all services


## Modules needed
* sys

all modules are normally installed using pip, like

pip install --upgrade <name>

## Services
Services can be added in the smsids.py source file, just add an array to the services like

* ["HTTPS", 443, RE.http_200]

Service name, port, response

response can be normal text 

## Loging
per default, all events get logged in a "pseudo"-Json style to /var/log/smsids_syslog.log


