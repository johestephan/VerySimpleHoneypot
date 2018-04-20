import socket
import sys
import threading
sys.path.append('./')
import logit
import syslog



def run(service, port, response=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveaddy = ('0.0.0.0', port)
    sock.bind(serveaddy)
    sock.listen(1)
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        try:
            msg = ""
            con,addy = sock.accept()
            data = con.recv(16000) # receive maximum 8K data
            dataarray = data.split('\n')
            #logit.log(service, addy[0], data)
            syslog.syslog('''%s-Honey| %s | %s''' % (service, addy[0], str(data)))
            con.send(response)
            con.close()
        except Exception, e:
            print e
