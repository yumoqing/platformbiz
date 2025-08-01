from testenv import runtest
from appPublic.dictObject import DictObject
from platformbiz.product import open_agree_account

async def test(sor):
	orgid = 'ac4HnQ0txGqmbAFWpI3wp'
	agreeid = 'NUvV1sP9TtAdnlxCISzjo'
	await open_agree_account(sor, orgid, '0')

if __name__ == '__main__':
	runtest(test)

