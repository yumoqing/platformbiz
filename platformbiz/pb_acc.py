import time
import json
from appPublic.timeUtils import timestampstr
from appPublic.registerfunction import rfexe
from sqlor.dbpools import DBPools
from ahserver.serverenv import get_serverenv
from accounting.accounting_config import Accounting
from accounting.bizaccount import BizAccounting
from accounting.bill import write_bill
from platformbiz.getdbname import get_dbname

async def get_owner_orgid(sor, orgid):
	return '0'

async def get_balance(orgid):
	db = DBPools()
	dbname = get_dbname()
	async with db.sqlorContext(dbname) as sor:
		f = get_serverenv('getCustomerBalance')
		if f:
			return await f(sor, orgid)
	return None

class PlatformBizAcc:
	"""
	"""
	async def build_accountset(self, sor, biz_order, biz_orderdetails):
		acconuntset = DictObject()
		accountset['action'] = biz_order.business_op
		accountset['owner'] = get_owner_orgid(sor, '0')
		accountset['reseller'] = biz_order.resellerid
		accountset['customer'] = biz_order.customerid
		accountset['交易金额'] = biz_order.amount
		transfee = await get_transfee(sor, self.resellerid, biz_order.amount, self.curdate)
		accountset['交易费用'] = transfee
		accountset.subsets = []
		for od in biz_orderdetails:
			price_infos = await get_price_infos(sor, self.resellerid, 
										self.customerid, 
										detail.productid, 
										detail.prod_config)
			if len(price_infos) > 1:
				for pi in price_infos[:-1]:
					actions = biz_order.business_op.split('_')
					actions[0] = actions[0] + '*'
					aset = DictObject()
					aset['action'] = '_'.join(actions)
					aset['owner'] = get_owner_orgid(sor, '0')
					aset['reseller'] = pi['buyerid']
					aset['provider'] = pi['resellerid']
					aset['采购成本'] = pi['sell_price']
					accountset.subsets.append(aset)
		return accountset
		
	async def accounting(self, sor, biz_orderid):
		biz_order = await sor.R('biz_order', {'id':biz_orderid})
		details = await sor.R('biz_orderdetail',{'orderid':biz_orderid})
		accountset = await self.build_accountset(biz_order, details)
		self.curdate = await get_business_date(sor)
		transfee = await get_transfee(sor, self.resellerid, biz_order.amount, self.curdate)
		a = BizAccounting(self.curdate, biz_order, accountset)
		r = await a.do_accounting(sor)
		
	async def get_orgid_by_trans_role(self, sor, orgtype):
		if orgtype== 'customer':
			return self.customerid
		if orgtype== 'reseller':
			return self.resellerid
		if orgtype== 'provider':
			return self.providerid
		if orgtype == 'owner':
			return '0'
		return None

class PlatformBizAccRecharge(PlatformBizAcc):
	def __init__(self, rlid):
		self.rlid = rlid

	async def accounting(self, sor):
		sql = """select * from recharge_log where id=${rlid}$"""
		recs = await sor.sqlExe(sql, {'rlid':self.rlid})
		if len(recs) < 1:
			e = Exception(f'get recharge log err by {rlid=}')
			exception(f'{e=}')
			raise e
		self.recharge = recs[0]
		self.customerid = self.recharge.customerid
		self.orderid = self.recharge.biz_orderid
		self.userid = self.recharge.userid
		get_business_date = get_serverenv('get_business_date')
		self.curdate = await get_business_date(sor)
		self.variable = {
			"交易金额":self.recharge.recharge_amt,
			"充值费率":self.recharge.fee_rate,
			"充值费用":self.recharge.feemat
		}
		bill = await write_bill(sor, self.customerid, self.userid, 
										self.recharge.orderid, 
										self.recharge.action, 
										self.recharge.recharge_amt)

		self.billid = bill.id
		self.bill = bill
		self.providerid = None
		self.resellerid = None
		self.action = self.recharge.action
		self.productid = None
		self.timestamp = timestampstr()
		a = Accounting(self)
		r = await a.do_accounting(sor)
		
