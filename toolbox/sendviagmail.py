import smtplib
import sys
fromaddr = ''
toaddrs  = ''
with open(sys.argv[1]) as infile:
	msg = str(infile.read())


# Credentials (if needed)
username = ''
password = ''

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
