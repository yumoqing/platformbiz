from testenv import runtest
from appPublic.dictObject import DictObject
from platformbiz.product import agree_products_clone

async def test(sor):
	orgid = 'ac4HnQ0txGqmbAFWpI3wp'
	agreeid = 'NUvV1sP9TtAdnlxCISzjo'
	await agree_products_clone(sor, orgid, agreeid)

if __name__ == '__main__':
	runtest(test)

