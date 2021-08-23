import requests
from fake_useragent import UserAgent
from pyvirtualdisplay import Display
from selenium import webdriver
import pandas as pd
# 開啟虛擬化界面
# display = Display(visible=0, size=(400, 300))
# display.start()

# driver = webdriver.Chrome()
# url = 'https://en.wikipedia.org/wiki/'

# driver.get(url)
# print(driver.current_url)

# before groupby, 用不到
def new_rank_before_groupby(df):
	page_num = df.shape[0]
	pre_rank = list(df['rank'])
	cur_rank = 1
	cummulated_same_count = 0
	df.loc[0, 'rank'] = cur_rank
	for i in range(1, page_num):
		if pre_rank[i-1] == pre_rank[i]:
			cummulated_same_count += 1
		else:
			cur_rank = cur_rank + 1 + cummulated_same_count
			cummulated_same_count = 0
		df.loc[i, 'rank'] = cur_rank

def new_rank(df):
	cur_rank = 1
	df.loc[0, 'rank'] = cur_rank
	cummulated_same_count = 0
	for i in df.index[1:]:
		if df.loc[i-1, 'views_ceil'] == df.loc[i, 'views_ceil']:
			cummulated_same_count += 1
		else:
			cur_rank = cur_rank + cummulated_same_count + 1
			cummulated_same_count = 0
		df.loc[i, 'rank'] = cur_rank

us_csv = pd.read_csv('0818/csv/US.csv')

us_group = us_csv[['article_transformed', 'views_ceil']].groupby('article_transformed').sum().sort_values('views_ceil', ascending=False)
us_group.reset_index(inplace=True)

new_rank(us_group)
print(us_group)