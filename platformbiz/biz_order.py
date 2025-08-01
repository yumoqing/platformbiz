from time import time
from ahserver.serverenv import get_serverenv
from sqlor.dbpools import DBPools
from appPublic.dictObject import DictObject
from appPublic.log import debug
from appPublic.uniqueID import getID
from platformbiz.const import ORDER_INITIAL, RECHARGE_INITIAL
from platformbiz.pricing import get_biz_date

async def add_recharge_order(sor, customerid, userid, action, recharge_amt):
	"""
	arguments:
		customerid: organization who recharge
		userid: user who do the recharge action
		recharge_amt: recharge amount
		action: business action name
	return:
		order record
	"""
	rec = DictObject()
	rec.id = getID()
	rec.customerid = customerid
	rec.userid = userid
	get_business_date = get_serverenv('get_business_date')
	rec.order_date = await get_business_date()
	rec.business_op = action
	rec.amount = recharge_amt
	rec.order_status = ORDER_INITIAL
	await sor.C('biz_order', rec.copy())
	return rec

async def get_paychannel_by_name(sor, name):
	sql = "select * from paychannel where name=${name}$"
	recs = await sor.sqlExe(sql, {'name':name})
	if len(recs) > 0:
		return recs[0]
	debug(f'get paychannel error({name})')
	return None

async def add_recharge_log(sor, customerid, userid, action, orderid, transdate, recharge_amt, name):
	rec = DictObject()
	rec.id = getID()
	rec.customerid = customerid
	rec.userid = userid
	rec.action = action
	rec.recharge_amt = recharge_amt
	pc = await get_paychannel_by_name(sor, name)
	debug(f'{pc=}, {recharge_amt=}')
	if pc is None:
		raise Exception(f'paychannel({name}) pay channel not found')
	rec.fee_amt = recharge_amt * pc.fee_rate
	rec.fee_rate = pc.fee_rate
	rec.pcid = pc.id
	rec.biz_orderid = orderid
	rec.recharge_status = RECHARGE_INITIAL
	rec.transdate = transdate
	await sor.C('recharge_log', rec.copy())
	return rec

async def change_recharge_status(sor, rlid, status, tid):
	recs = await sor.R('recharge_log', {'id':rlid})
	if len(recs) < 1:
		return None
	recs[0].recharge_status = status
	recs[0].channel_tid = tid
	await sor.U('recharge_log', recs[0].copy())
	return recs[0]


async def add_pay_order(sor, sellerid, 
						customerid, 
						userid, 
						action, 
						order_details, 
						origin_orderid=None):
	env = globals()
	customerid1 = await env.get_userorgid()
	userid1 = await env.get_user()
	if customerid != customerid1:
		e = Exception(f'{custmerid} is not logined orgid')
		exception(f'{e}')
		raise e
	if userid != userid1:
		e = Exception(f'{userid} is not logined userid')
		exception(f'{e}')
		raise e
	id = getID()
	amount = 0.0
	for order_detail in order_details:
		ns1 = {
			"id": id,
			"orderid":ns['id'],
			"productid":order_detail.productid,
			"product_cnt":order_detail.product_cnt,
			"prod_config":order_detail.prod_config,
			"list_amount":order_detail.list_amount,
			"trans_amount":order_detail.trans_amount
		}
		await sor.C('biz_orderdetail', ns1)
		amount += order_detail.trans_amount
		price_infos = await get_price_infos(sor, sellerid, 
									customerid, 
									order_detail.productid, 
									order_detail.prod_config)
		
		
	ns = {
		"id": id,
		"customerid":customerid,
		"userid":userid,
		"resellerid":sellerid,
		"order_date":await get_biz_date(sor),
		"order_status":"0",
		"business_op":action,
		"amount":pay_amount,
		"ordertype":None,
		"pay_date":None,
		"origin_orderid":origin_orderid
	}
	await sor.C('biz_order', ns)

