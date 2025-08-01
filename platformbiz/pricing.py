
from appPublic.log import debug, exception
from ahserver.serverenv import get_serverenv
from traceback import format_exc

def get_step_dates(use_date, step_type):
	if step_type == '0':
		# 总金额
		return '1000-01-01', '9999-12-31'
	y = int(use_date[:4])
	m = int(use_date[6:7])
	if step_type == '1':
		y = int(use_date[:4])
		return '%04d-01-01' % y, '%04d-01-01' % (y+1)
	if step_type == '2':
		ss = [1,4,7,10, 13]
		for i, s in enumerate(ss):
			if m >=s and m < ss[i+1]:
				if i < 3:
					return '%04d-%02d-01' % (y, s), '%04d-%02d-01' % (y, ss[i+1])
				else:
					return '%04d-%02d-01' % (y, s), '%04d-01-01' % (y+1)
	if step_type == '3':
		if m < 12:
			return '%04d-%02d-01' % (y, m), '%04d-%02d-01' % (y, m+1)
		else:
			return '%04d-%02d-01' % (y, m), '%04d-01-01' % (yi+1)
	e = Exception(f'unknown {step_type=}')
	exception(f'{e=}')
	raise e

async def get_biz_date(sor):
	biz_date = ''
	f = get_serverenv('get_business_date')
	if f:
		biz_date = await f(sor)
		return biz_date
	e = Exception(f'get_serverenv("get_business_date") return None')
	exception(f'{e=}')
	raise e
	
async def get_step_discount(sor, agreedetailid, step_type, sellerid, buyerid):
	amount = await get_sale_amount(sor, step_type, sellerid, buyerid)
	sql = """select * from agreedetailstep
where adid = ${adid}
	and minamt <= ${amount}$
	and maxamt > ${amount}$
"""
	recs = await sor.sqlExe(sql, {'adid':agreedetailid,
			'amount':amount
	})
	if len(recs) < 1:
		e = Exception(f'{sql=} not data, {agreedetailid=}, {amount=}')
		exception(f'{e=}')
		raise e
	return rec.discount

async def get_sale_amount(sor, step_type, sellerid, buyerid):
	"""
	统计销售收入，根据step_type分别统计总销售额，本年销售累计
	本季度销售累计，本月销售累计和本周销售累计等
	"""
	subjectname = '供应商分销收入'
	f = get_serverenv('getAccountByName')
	if f is None:
		e = Exception(f'get_serverenv("getAccountByName") return None')
		exception(f'{e=}')
		raise e
	
	acc = await f(sor, accounting_orgid, sellerid, subjectname, buyerid)
	biz_date = await get_biz_date(sor)
	from_date, to_date = get_date_between(biz_date, step_type)
	f = get_serverenv('get_account_total_amount')
	if f is None:
		e = Exception(f'get_serverenv("get_account_total_amount") return None')
		exception(f'{e=}')
		raise e
	amount = await f(sor, acc.id, acc.blance_at, from_date, to_date)
	return amount
	
async def get_product_agreement(sor, sellerid, buyerid, productid, biz_date):
	sql = """select a.*, 
c.id as agreedetailid,
c.prodtypeid as agree_prodtypeid,
c.discount,
c.step_type
from product as a, agreement as b, agreedetail as c
where c.agreeid = b.id
    and ( a.prodtypeid = c.prodtypeid or c.prodtypeid is NULL)
    and a.orgid = b.providerid
    and b.enable_date <= ${biz_date}$
    and b.expire_date > ${biz_date}$
    and a.orgid = ${sellerid}$
    and b.resellerid = ${buyerid}$
    and a.id = ${productid}$
"""
	recs = await sor.sqlExe(sql, {'sellerid':sellerid,
			'buyerid':buyerid,
			'biz_date':biz_date,
			'productid':productid
	})
	if len(recs) == 0:
		e = f'there is no agreement for {sellerid=} and {buyerid=}, {productid=} at {biz_date=} {sql=}'
		debug(f'{e=}')
		return None
	rec = None
	for r in recs:
		if r.prodtypeid == r.agree_prodtypeid:
			rec = r
			break
	if rec is None:
		for r in recs:
			if r.agree_prodtypeid is None:
				rec = r
				break
	if rec is None:
		e = Exception(f'Not agreements for {sellerid=} and {buyerid=}, {productid=} at {biz_date=} ') 
		exception(f'{e=}')
		raise e
	return rec

def get_unit_value_price(sc, pricingtab):
	for pt in pricingtab:
		if pt.specvalue == '':
			pt.specvalue = None
		if sc.spec_name == pt.specname and \
				sc.spec_value == pt.specvalue:
			# print(f'found {sc.spec_name=},{sc.spec_value=}')
			return pt.unit_value, pt.unit_amt
		# print(f'{sc.spec_name=},{sc.spec_value=}:{pt.specname=},{pt.specvalue=}')
	return None, None

async def calc_prod_price(sor, productid, spec_config):
	"""fact_config:
	[
		{
			spec_name, spec_value, count
		}
	]	
	"""
	biz_date = await get_biz_date(sor)
	sql = """select c.*,
e.name as specname
from product a, prodpricing b, 
		prodpricingtab c, prodtype d, 
		prodtypespec e
where a.id=${productid}$
	and a.prodtypeid = d.id
	and e.prodtypeid = d.id
	and a.id = b.prodid
	and b.enable_date <= ${biz_date}$
	and b.expire_date > ${biz_date}$
	and c.prodpricingid = b.id
	and c.ptspecid = e.id
"""
	recs = await sor.sqlExe(sql, {'productid':productid, 
					'biz_date':biz_date})

	if len(recs) < 1:
		e = Exception(f'{sql=}, {productid=} {biz_date=} return not data')
		exception(f'{e=}')
		raise e
	price = 0.0
	for sc in spec_config:
		# print(f'{sc=}, {recs=}')
		uv, up = get_unit_value_price(sc, recs)
		if uv is None:
			continue
		cnt = sc.count / uv
		price += up * cnt
	return price

async def get_sell_price(sor, sellerid, buyerid, productid, list_price):
	"""
	获得商品售价
	"""
	
	biz_date = await get_biz_date(sor)
	agree = await get_product_agreement(sor, sellerid, buyerid, productid, biz_date)
	if agree is None:
		return list_price
 
	debug(f'{agree=}')
	if agree.discount:
		return list_price * agree.discount
	discount = await get_step_discount(sor, agree.agreedetailid, agree.step_type, selllerid, buyerid)
	debug(f'step {discount=}')
	return discount * list_price

async def get_price_infos(sor, sellerid, buyerid, productid, prod_config):
	"""
	获得商品价格
	resellerid:商户id
	productid:商品id
	prod_config:商品配置
	返回
		[
			{ownerid, list_price, price}, ...
		]
	"""
	cost_pricing_infos = []
	sql1 = """select a.*, 
b.pricing_method,
b.apiid
from product a left join prodpricing b on a.id=b.prodid 
where a.id = ${productid}$ 
	and a.orgid = ${sellerid}$"""
	prods = await sor.sqlExe(sql1, {'productid':productid, 'sellerid':sellerid})
	if len(prods) < 1:
		e = Exception(f'{resellerid=} {productid=} product not found')
		exception(f'{e=}')
		raise e
	prod = prods[0]
	if prod.agreeid is not None:
		cost_pricing_infos = await get_price_infos(sor, prod.providerid, sellerid, prod.providerpid, prod_config)

	if prod.pricing_method == '0':
		# 按资源因子计费
		list_price = await calc_prod_price(sor, productid, prod_config)
		sell_price = await get_sell_price(sor, sellerid, buyerid, productid, list_price)
		pricing_info = {
			'sellerid': sellerid,
			'buyerid': buyerid,
			'productid': productid,
			'list_price': list_price,
			'sell_price': sell_price
		}
	elif prod.pricing_method == '1':
		# 外部计费
		f = get_serverenv('pricing_api')
		list_price = await f(sor, prod.apiid, providerpid, prod_config)
		sell_price = await get_sell_price(sor, sellerid, buyerid, productid, list_price)
		pricing_info = {
			'sellerid': sellerid,
			'buyerid': buyerid,
			'productid': productid,
			'list_price': list_price,
			'sell_price': sell_price
		}
	else:
		# 供应商计费
		if len(cost_pricing_infos) < 1:
			e = Exception(f'{sellerid=}, {buyerid=}, {productid=} has not resell agreement')
			exception(e)
			raise e
		list_price = cost_pricing_infos[-1]['list_price']
		sell_price = await get_sell_price(sor, sellerid, buyerid, productid, list_price)
		pricing_info = {
			'sellerid': sellerid,
			'buyerid': buyerid,
			'productid': productid,
			'list_price': list_price,
			'sell_price': sell_price
		}
	if len(cost_pricing_infos) > 0:
		pricing_info['cost_price'] = cost_pricing_infos[-1]['sell_price']
	cost_pricing_infos.append(pricing_info)
	return cost_pricing_infos

async def get_transfee(sor, resellerid, transamt, biz_date):
	sql = """select * from reseller 
where orgid=${resellerid}$ 
	and enable_date<=${biz_date}$
	and expire_date>${biz_date}$
"""
	recs = sor.sqlExe(sql, {'resellerid':resellerid, 'biz_date':biz_date})
	if len(recs) < 1:
		e = Exception(f'reseller(id={resellerid}) not available at {biz_date=}')
		exception(f'{e=}')
		raise e
	rate =  recs[0].transrate
	return transamt * rate

