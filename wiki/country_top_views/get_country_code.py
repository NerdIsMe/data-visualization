import requests, json
import pandas as pd
from lxml import etree
from fake_useragent import UserAgent
iso_3166_url = 'https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes'

response = requests.get(iso_3166_url)
html = etree.HTML(response.text)

countries_table = html.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody')[0]

countries_pd = pd.DataFrame(data={'country name':[], 'official state name':[], 'country code':[], 'wiki stats':[]})
countries_pd_index = 0
for country_i in countries_table.xpath('./tr')[2:]:
	try:
		country_name = country_i.xpath('./td[1]/a/text()')[0]
		official_state_name = country_i.xpath('./td[2]/a/text()')[0]
		country_code = country_i.xpath('./td[4]/a/span/text()')[0]
	except:
		continue
	countries_pd.loc[countries_pd_index, 'country name'] = country_name
	countries_pd.loc[countries_pd_index, 'official state name'] = official_state_name
	countries_pd.loc[countries_pd_index, 'country code'] = country_code

	# get country top views 2021/08/18
	url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top-per-country/%s/all-access/2021/08/18' %country_code
	top1000 = requests.get(url, headers={'user-agent': UserAgent().random})
	top_dict = top1000.json()
	if 'title' in top_dict and top_dict['title'] == 'Not found.': # 該國資料不存在
		countries_pd.loc[countries_pd_index, 'wiki stats'] = False
	else:
		with open('./0818/%s.json' %country_code, 'w') as f:
			json.dump(top_dict, f)
		countries_pd.loc[countries_pd_index, 'wiki stats'] = True

	countries_pd_index += 1
	print(', '.join([country_name, official_state_name, country_code]))

print(countries_pd)
countries_pd.to_csv('country_code.csv', index = False)