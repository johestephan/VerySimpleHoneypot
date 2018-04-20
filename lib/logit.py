# --- UNUSED ----


import sys
sys.path.append('../modules/')
import datetime
import time

def write_out(dataset, file="/var/log/smsids_syslog.log"):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    with open(file, "ab") as mylogf:
        mylogf.write("%s -- %s\n" %(st, dataset))
    mylogf.close()
    
def log(agent, ip, data):
    dataset = {agent : [ip, data]}
    write_out(str(dataset))
