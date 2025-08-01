
from testenv import runtest
from appPublic.dictObject import DictObject
from platformbiz.pricing import get_price_infos

async def test(sor):
	# prodid = 'a--akNeu1Ia-NOZAJAadf'
	prodid = '1wleQ7o-RkrSbR-n368bO'
	buyerid = 'yyoJwfBDsRiwN8-WFl2q1'
	sellerid = '0'
	spec_config = [
		DictObject(**{
			"spec_name":"input_tokens",
			"count":12832
		}),
		DictObject(**{
			"spec_name":"output_tokens",
			"count":786323
		})
	]
	d = await get_price_infos(sor, sellerid, buyerid, prodid, spec_config)
	print(f'{d=}')

if __name__ == '__main__':
	runtest(test)

