from ahserver.serverenv import ServerEnv, get_serverenv
from platformbiz.recharge import Recharge
from platformbiz.pb_acc import PlatformBizAccRecharge, get_owner_orgid, get_balance
from platformbiz.biz_order import change_recharge_status
from platformbiz.pricing import calc_prod_price, get_sell_price, get_price_infos
from platformbiz.product import agree_products_clone, open_agree_account

def load_platformbiz():
	g = ServerEnv()
	g.Recharge = Recharge
	g.PlatformBizAccRecharge = PlatformBizAccRecharge
	g.change_recharge_status = change_recharge_status
	g.get_owner_orgid = get_owner_orgid
	g.get_balance = get_balance
	g.calc_prod_price = calc_prod_price
	g.get_sell_price = get_sell_price
	g.get_price_infos = get_price_infos
	g.agree_products_clone = agree_products_clone
	g.open_agree_account = open_agree_account

