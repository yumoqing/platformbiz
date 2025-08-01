import os
import asyncio
from appPublic.jsonConfig import getConfig
from sqlor.dbpools import DBPools
from appbase.init import load_appbase
from accounting.init import load_accounting
from platformbiz.init import load_platformbiz

async def main(asyncfunc):
	home = os.environ['HOME']
	p = f'{home}/py/sage'
	config = getConfig(p, {'workdir':p})
	db = DBPools(config.databases)
	load_appbase()
	load_accounting()
	load_platformbiz()
	async with db.sqlorContext('sage') as sor:
		await asyncfunc(sor)
	
def runtest(asyncfunc):
	asyncio.new_event_loop().run_until_complete(main(asyncfunc))

	
