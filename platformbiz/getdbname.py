from ahserver.serverenv import get_serverenv

def get_dbname():
	f = get_serverenv('get_module_dbname')
	if f is None:
		raise Exception('get_module_dbname() not found')
	return f('platformbiz')

