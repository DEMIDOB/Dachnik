def get_all_products():
	from requests import get
	import json

	req_res = get("https://694536d7edf9.ngrok.io/DBs/ru_RU/odata/standard.odata/Catalog_%D0%A2%D0%BE%D0%B2%D0%B0%D1%80%D1%8B?$format=json")
	if not req_res.ok:
		return get_all_products()
	json_data = json.loads(req_res.text)
	return json_data['value']

if __name__ == "__main__":
	products = get_all_products()
	# print(products)
	for pr in products:
		print(pr['Description'], pr['Category'])
