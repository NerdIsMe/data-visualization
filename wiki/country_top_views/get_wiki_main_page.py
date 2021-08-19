import pandas as pd 
from lxml import etree
import requests

url = 'https://en.wikipedia.org/wiki/List_of_Wikipedias'

response = requests.get(url)
html = etree.HTML(response.text)

lang_codes = []
lang_url_names = []
table_contents = html.xpath('//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr')
for i in table_contents[1:]:
	print(etree.tostring(i, method='html'))
	lang_code = i.xpath('./td[2]/a/text()')[0]
	lang_url_name = i.xpath('./td[2]/a/@href')[0]#.split('/')# [-1]
	print(lang_code)
	print(lang_url_name)
	lang_codes.append(lang_code)
	lang_url_names.append(lang_url_name)

results = pd.DataFrame()
results['lang_code'] = lang_codes
results['lang_url_names'] = lang_url_names

result.to_csv('wiki_main_page.csv')