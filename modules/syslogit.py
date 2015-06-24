import logging
import logging.handlers

def logit(AGENT, data):
	try:
		data = map(str.strip, data)
		sm = logging.getLogger(AGENT)
		sm.setLevel(logging.INFO)
		h = logging.handlers.SysLogHandler(address = ('localhost',514),facility=logging.handlers.SysLogHandler.LOG_LOCAL6)
		sm.addHandler(h)

		sm.info(AGENT + " " + " ".join(data))
		return 1	
	except:
		print err
		return 0
