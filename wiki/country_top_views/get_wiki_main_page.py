import pandas as pd 
from lxml import etree
import requests
from pyvirtualdisplay import Display
from selenium import webdriver
from urllib.parse import unquote

url = 'https://en.wikipedia.org/wiki/List_of_Wikipedias'

response = requests.get(url)
html = etree.HTML(response.text)

lang_codes = []
lang_urls = []
lang_main_pages = []

# get main page url
table_contents = html.xpath('//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr')
for i in table_contents[1:]:
	lang_code = i.xpath('./td[2]/a/text()')[0]
	lang_url = i.xpath('./td[2]/a/@href')[0]#.split('/')# [-1]
	lang_codes.append(lang_code)
	lang_urls.append(lang_url)

# get main page name
display = Display(visible=0, size=(400, 300))
display.start()
driver = webdriver.Chrome()
# en url 有點問題，直接跳過
i = 2
lang_main_pages.append('Main_Page')
for lang_url in lang_urls[1:]:
	driver.get(lang_url)
	main_page = unquote(driver.current_url).split('/')[-1]#.encode('utf-8')
	lang_main_pages.append(main_page)

	print(i, lang_codes[i-1], main_page)
	i += 1

display.stop()

results = pd.DataFrame()
results['lang_code'] = lang_codes
results['lang_url'] = lang_urls
results['main_page'] = lang_main_pages

results.to_csv('wiki_main_page.csv')