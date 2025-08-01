from appPublic.uniqueID import getID
from appPublic.log import debug
from accounting.openaccount import openRetailRelationshipAccounts

async def get_accounting_orgid(sor):
	return '0'

async def agree_products_clone(sor, orgid, agreeid):
	"""
	adid:agreedetailid
	sor:
	return None
	"""
	sql = """select a.id,
a.name,
a.prodtypeid,
a.description,
a.prod_state,
a.product_code,
a.spec_note,
b.id as apid,
d.id as agreeid,
d.providerid,
d.resellerid
from product a, agreeproduct b, agreedetail c, agreement d
where a.id = b.providerpid
	and b.resellerpid is null
	and c.id = b.agreedetailid
	and d.id = c.agreeid
	and d.id = ${agreeid}$
	and a.orgid = ${orgid}$
"""
	recs = await sor.sqlExe(sql, {'agreeid':agreeid, 'orgid':orgid})
	if len(recs) < 1:
		debug(f'{orgid=}, {agreeid=}, {sql=}: found no data')
		return
	
	for rec in recs:
		pid = getID()
		d = {
			"id":pid,
			"name":rec.name,
			"prodtypeid":rec.prodtypeid,
			"orgid":rec.resellerid,
			"providerid":rec.providerid,
			"agreeid":rec.agreeid,
			"providerpid":rec.id,
			"description":rec.description,
			"prod_state":rec.prod_state,
			"product_code":rec.product_code,
			"spec_note":rec.spec_note
		}
		await sor.C('product', d)
		await sor.U('agreeproduct', {'id':rec.apid, 'resellerpid':pid})

async def open_agree_account(sor, providerid, sellerid):
	accounting_orgid = await get_accounting_orgid(sor)
	await openRetailRelationshipAccounts(sor, accounting_orgid, providerid, sellerid)

