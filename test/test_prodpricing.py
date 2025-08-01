from testenv import runtest
from appPublic.dictObject import DictObject
from platformbiz.pricing import calc_prod_price

async def test(sor):
	# prodid = 'a--akNeu1Ia-NOZAJAadf'
	prodid = 'MT-k34zPUAuWqgov4QCmG'
	spec_config = [
		DictObject(**{
			"spec_name":"input_tokens",
			"count":12832
		})#,
		#DictObject(**{
		#	"spec_name":"output_tokens",
		#	"count":786323
		#})
	]
	price = await calc_prod_price(sor, prodid, spec_config)
	print(f'{prodid=}, {spec_config=}, {price=}')

if __name__ == '__main__':
	runtest(test)

