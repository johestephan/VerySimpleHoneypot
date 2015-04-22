import logging
import logging.handlers

def logit(AGENT, data):
	try:
		sm = logging.getLogger(AGENT)
		sm.setLevel(logging.INFO)
		h = logging.handlers.SysLogHandler(address = '/dev/log')
		sm.addHandler(h)

		sm.info(AGENT + " " + " ".join(data))
		return 1	
	except:
		return 0
