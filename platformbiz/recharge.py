from accounting.accounting_config import Accounting
from appPublic.registerfunction import rfexe
from appPublic.log import exception, debug
from sqlor.dbpools import DBPools
from pf_pay.ali_pay import Zhifubao_Pay
from pf_pay.wechat_pay_h5 import WechatPayClient
from platformbiz.getdbname import get_dbname
from platformbiz.biz_order import add_recharge_log, add_recharge_order

class Recharge:
	def __init__(self, customerid, userid, recharge_amt, pc_name):
		self.customerid = customerid
		self.userid = userid
		self.recharge_amt = recharge_amt
		self.pc_name = pc_name

	async def start_recharge(self):
		return await self.start_recharge_action('RECHARGE')

	async def start_recharge_action(self, request, action):
		db = DBPools()
		dbname = get_dbname()
		async with db.sqlorContext(dbname) as sor:
			order = await add_recharge_order(sor, self.customerid,
											self.userid,
											action,
											self.recharge_amt)
			if order is None:
				return None
			rl = await add_recharge_log(sor, self.customerid,
											self.userid,
											action,
											order.id,
											order.order_date,
											self.recharge_amt,
											self.pc_name)
			if self.pc_name == 'alipay':
				z = Zhifubao_Pay()
				url = await z.alipay_payment(rl.id, rl.recharge_amt, action)
				return url
			if self.pc_name == 'wxpay':
				wxp = WechatPayClient()
				url = await wxp.create_h5_url(request, rl, action)
				return url

			exception(f'exception ...........{self.pc_name}')
			raise Exception(f'{self.pc_name} pay channel not implemented')
		exception('Exception happend ....')
	
		
