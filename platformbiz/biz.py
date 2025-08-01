from platformbiz.pricing import get_price_infos
from biz_order import add_pay_order

async customerpay(sor, sellerid, customerid, userid, order_details):
	await add_pay_order(sor, sellerid, customerid, userid, order_details)
	price_infos = await get_price_infos(sor, sellerid, 
										customerid, 
										priductid, 
										prod_config)
	:
