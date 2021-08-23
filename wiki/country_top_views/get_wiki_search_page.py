import pandas as pd 
from lxml import etree
import requests, time, random
from pyvirtualdisplay import Display
from selenium import webdriver
from urllib.parse import unquote

lang_code_pd = pd.read_csv('./wiki_main_page.csv')
lang_code_list = list(lang_code_pd['lang_code'])


search_pages = []
# get search page name
display = Display(visible=0, size=(400, 300))
display.start()
driver = webdriver.Chrome()

i = 0
for lang_code in lang_code_list:
	print(i, lang_code, end=' ')
	lang_url = 'https://%s.wikipedia.org/wiki/Special:Search' % lang_code
	driver.get(lang_url)
	search_page = unquote(driver.current_url).split('/')[-1]#.encode('utf-8')
	search_pages.append(search_page)

	i += 1
	print(search_page)
	time.sleep(random.randint(5, 15))
display.stop()

results = pd.DataFrame()
results['lang_code'] = lang_code_list
results['search_page'] = search_pages

results.to_csv('wiki_search_page.csv')