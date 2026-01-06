from ahserver.serverenv import ServerEnv, get_serverenv
from platformbiz.product import agree_products_clone, open_agree_account

def load_platformbiz():
	g = ServerEnv()
	g.agree_products_clone = agree_products_clone
	g.open_agree_account = open_agree_account

