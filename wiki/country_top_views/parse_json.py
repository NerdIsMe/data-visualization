import json, os, requests
import pandas as pd 

def title_transform(title, from_lang, to_lang='en'):
	url = "https://%s.wikipedia.org/w/api.php" %from_lang
	PARAMS = {
		"action": "query",
		"titles": title,
		"prop": "langlinks",
		"format": "json",
		"lllang": to_lang,
	}
	response = requests.get(url=url, params=PARAMS)
	response_dict = response.json()
	result = list((response_dict['query']['pages']).values())[0]
	# 找翻譯結果
	if 'langlinks' in result: # 有 to_lang 的結果
		transform_result = result['langlinks'][0]['*']
	else: # 沒有 to_lang 的結果，直接 return title
		transform_result = title
	
	return transform_result

files_dir = './0818/json'
files = os.listdir(files_dir)
# print(files)

file_path = files_dir + '/' + 'TW.json'

with open(file_path, 'r') as f:
	file = json.load(f)

rankings = pd.DataFrame.from_dict(file['items'][0]['articles'])
rankings.set_index('article', inplace=True)

for article_name in rankings.index:
	lang_project = rankings.loc[article_name, 'project']
	from_lang = lang_project.split('.')[0]
	transform_result = title_transform(article_name, from_lang)
	rankings.loc[article_name, 'article_transformed'] = transform_result
	print(rankings)

