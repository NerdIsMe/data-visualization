import json, os, requests, time
import pandas as pd 
from fake_useragent import UserAgent

def title_transform(title, from_lang, to_lang='en'):
	# if from_lang == to_lang, 直接 return
	if from_lang == to_lang:
		return title

	# time.sleep(time_sleep)

	url = "https://%s.wikipedia.org/w/api.php" %from_lang
	PARAMS = {
		"action": "query",
		"titles": title,
		"prop": "langlinks",
		"format": "json",
		"lllang": to_lang,
	}
	response = requests.get(url=url, params=PARAMS, headers={'user-agent': UserAgent().random})
	response_dict = response.json()
	result = list((response_dict['query']['pages']).values())[0]
	# 找翻譯結果
	if 'langlinks' in result: # 有 to_lang 的結果
		transform_result = result['langlinks'][0]['*']
	else: # 沒有 to_lang 的結果，直接 return title
		transform_result = title
	
	return transform_result

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
	
# open main_page file & search page file
main_page = pd.read_csv('./wiki_main_page.csv')
search_page = pd.read_csv('./wiki_search_page.csv')
main_page_list = list(main_page.main_page)
search_page_list = list(search_page.search_page)

files_dir = './0818/json'
save_dir = './0818/csv'
files = os.listdir(files_dir)

for file_i in files:
	print(file_i, end=', ')

	if os.path.exists('%s/%s.csv' %(save_dir, file_i[:2])):
		print('CSV file existed.')
		continue

	# open JSON file
	file_path = files_dir + '/' + file_i
	with open(file_path, 'r') as f:
		file = json.load(f)

	rankings = pd.DataFrame.from_dict(file['items'][0]['articles'])
	# rankings.set_index('article', inplace=True)

	former_index = list(rankings.index)
	for index in former_index:
		article = rankings.loc[index, 'article']
		# 如果是 wiki 首頁 or special:search 的話，跳過且刪除
		if article in main_page_list or article in search_page_list:
			rankings.drop(index, inplace=True)
			continue

		lang_project = rankings.loc[index, 'project']
		# MediaWiki project 都跳過，project 必須擁有 ".wikipedia" 的詞
		if '.wikipedia' not in lang_project:
			rankings.drop(index, inplace=True)
			continue
		from_lang = lang_project.split('.')[0]
		# print('from lang: %s, article: %s' %(from_lang, article))
		transform_result = title_transform(article, from_lang)
		rankings.loc[index, 'article_transformed'] = transform_result

	# group by article transform
	# 如果沒有文章瀏覽次數，直接跳過該國 
	if 'article_transformed' not in rankings.columns:
		print('skipped.')
		continue
	
	rankings_group = rankings[['article_transformed', 'views_ceil']].groupby('article_transformed').sum().sort_values('views_ceil', ascending=False)
	rankings_group.reset_index(inplace=True)

	new_rank(rankings_group)

	rankings_group['rank'] = rankings_group['rank'].astype(int)
	rankings_group.to_csv('%s/%s.csv' %(save_dir, file_i[:2]), index=False)
	print('done.')
